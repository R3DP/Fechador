"""`sellbird inboxes`: connect and run the extra inboxes you send from.

Nothing here prints a token or password. SMTP passwords are asked for with
getpass, and there is deliberately no password argument: it would land in
shell history.
"""

from __future__ import annotations

import argparse
import asyncio
import getpass
import sys
from datetime import date

from sellbird.mailboxes import (
    HARD_MAX_INBOX_CAP, MAIN, ConnectRefused, MailboxStore, build_provider,
    check_provider_allows_inboxes, connect_oauth_mailbox, connect_smtp_mailbox, load_inboxes,
)
from sellbird.secrets import SecretStore, SecretStoreUnavailable

MAIN_NAME = "main"   # how the main mailbox is named on the command line


def _date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError("use a real date, YYYY-MM-DD") from None


def _cap(value: str):
    if value == "default":
        return None
    try:
        cap = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("a whole number, or 'default'") from None
    if not 1 <= cap <= HARD_MAX_INBOX_CAP:
        raise argparse.ArgumentTypeError(f"between 1 and {HARD_MAX_INBOX_CAP}")
    return cap


def register(subparsers) -> None:
    sub = subparsers.add_parser("inboxes", help="Conectar e gerenciar as caixas de e-mail das quais você envia")
    actions = sub.add_subparsers(dest="inboxes_action")

    actions.add_parser("list", help="Cada caixa, seu estado e os envios frios de hoje")

    connect = actions.add_parser("connect", help="Conectar uma caixa que você já tem")
    kinds = connect.add_subparsers(dest="kind", required=True)
    for kind in ("gmail", "microsoft", "smtp"):
        p = kinds.add_parser(kind)
        p.add_argument("--address", required=True, help="O endereço de e-mail da caixa")
        p.add_argument("--name", default="", help="Nome mostrado em From (padrão: persona.name)")
        p.add_argument("--warmup-started", default="", type=_date, metavar="YYYY-MM-DD",
                       help="Quando esta caixa começou a aquecer (omita se já estabelecida)")
        if kind == "smtp":
            p.add_argument("--smtp-host", required=True)
            p.add_argument("--smtp-port", type=int, default=587)
            p.add_argument("--username", default="", help="Padrão: o próprio endereço")
            p.add_argument("--imap-host", default="", help="Padrão: o host SMTP")
            p.add_argument("--imap-port", type=int, default=993)

    test = actions.add_parser("test", help="Verificar se uma caixa consegue fazer login")
    test.add_argument("address")

    pause = actions.add_parser("pause", help="Parar de enviar de uma caixa")
    pause.add_argument("address")
    pause.add_argument("--reason", default="pausado por você")
    resume = actions.add_parser("resume", help="Voltar a enviar de uma caixa pausada")
    resume.add_argument("address")

    cap = actions.add_parser("cap", help="Definir o limite diário de e-mail frio de uma caixa")
    cap.add_argument("address")
    cap.add_argument("cap", type=_cap, help=f"1-{HARD_MAX_INBOX_CAP}, ou 'default'")

    name = actions.add_parser("name", help="Mudar o nome com que uma caixa envia")
    name.add_argument("address")
    name.add_argument("name")

    remove = actions.add_parser(
        "remove", help="Parar de usar uma caixa definitivamente (o login continua no seu keychain)")
    remove.add_argument("address")

    use = actions.add_parser(
        "use", help="Escolher de quais caixas uma campanha envia (nenhuma: todas as caixas)")
    use.add_argument("campaign", help="Id da campanha ou nome exato")
    use.add_argument("addresses", nargs="*",
                     help=f"Endereços de caixa; '{MAIN_NAME}' é sua caixa principal")
    sub.set_defaults(func=cmd_inboxes)


async def print_inbox_list(store: MailboxStore, config, env) -> None:
    from sellbird.integrations.mail_provider import NATIVE_PROVIDERS, get_mail_provider

    main = get_mail_provider(config, env) \
        if config.channels.email.provider in NATIVE_PROVIDERS else None
    inboxes = await load_inboxes(store, config, env, main)
    if not inboxes.inboxes:
        print("\n  Nenhuma caixa: seu provedor de envio é "
              f"{config.channels.email.provider or 'não definido'}.\n")
        return
    print(f"\n  {'Caixa':38} {'Estado':16} Frios hoje")
    for inbox in inboxes.inboxes.values():
        label = f"{inbox.address or '(caixa principal)'}{' (principal)' if inbox.main and inbox.address else ''}"
        if not inbox.connected:
            state = "não conectada"
        elif inbox.paused_reason:
            state = "pausada"
        else:
            state = "enviando"
        print(f"  {label:38} {state:16} {inbox.sent_today}/{inbox.cap}")
        if inbox.paused_reason:
            print(f"  {'':38} {inbox.paused_reason}")
    if not inboxes.several:
        print("\n  Adicione outra com: sellbird inboxes connect gmail|microsoft|smtp --address ...")
    print(f"\n  Tudo que foi enviado hoje fica dentro de max_daily_sends "
          f"({config.channels.email.max_daily_sends}).\n")


async def _test_and_print(provider) -> bool:
    try:
        ok, detail = await provider.test_connection()
    except Exception as e:
        ok, detail = False, f"Couldn't check the connection ({type(e).__name__})"
    print(f"\n  {'✓' if ok else '✗'} {detail}\n")
    return ok


def _oauth_sign_in(args, env) -> dict | None:
    """Run the browser sign-in; the token stays in memory until it's stored."""
    captured: dict = {}
    if args.kind == "gmail":
        from sellbird.integrations.gmail import run_auth_flow
        ok = run_auth_flow(env.gmail_client_id, env.gmail_client_secret,
                           save=captured.update, expected_address=args.address)
    else:
        from sellbird.integrations.microsoft import run_auth_flow
        ok = run_auth_flow(env.m365_client_id, env.m365_tenant_id,
                           save=captured.update, expected_address=args.address)
    return captured if ok and captured else None


def read_smtp_password(args) -> str:
    return getpass.getpass(f"Senha SMTP para {args.address}: ")


async def connect_flow(args, store: MailboxStore, secrets: SecretStore, config, env) -> int:
    from sellbird.integrations.smtp_mail import SmtpSettings

    try:
        check_provider_allows_inboxes(config)
        common = dict(address=args.address, display_name=args.name,
                      warmup_started_at=args.warmup_started or "")
        if args.kind == "smtp":
            settings = SmtpSettings(
                host=args.smtp_host, username=args.username or args.address.strip().lower(),
                password=read_smtp_password(args), port=args.smtp_port,
                imap_host=args.imap_host, imap_port=args.imap_port)
            mailbox_id = await connect_smtp_mailbox(store, secrets, config, settings=settings,
                                                    **common)
        else:
            token = _oauth_sign_in(args, env)
            if token is None:
                print("\n  O login não foi concluído, então nada foi conectado.\n")
                return 1
            provider = "google" if args.kind == "gmail" else "microsoft"
            mailbox_id = await connect_oauth_mailbox(store, secrets, config, provider=provider,
                                                     token=token, **common)
    except (ConnectRefused, SecretStoreUnavailable) as e:
        print(f"\n  {e}\n")
        return 1

    print(f"\n  Conectado {args.address.strip().lower()}.")
    if config.channels.email.max_daily_sends <= config.channels.email.per_inbox_daily_cap:
        print("  Nota: max_daily_sends limita tudo que é enviado em um dia em todas as caixas. "
              "Aumente no sellbird.yaml para que esta caixa contribua ao que sai.")
    row = await store.get_mailbox(mailbox_id)
    provider = build_provider(row, config=config, env=env, secrets=secrets)
    if provider is None:
        print("  Não foi possível montar uma conexão para testar.\n")
        return 1
    return 0 if await _test_and_print(provider) else 1


async def _find(store: MailboxStore, address: str) -> dict | None:
    row = await store.get_mailbox_by_address(address)
    if row is None or row.get("state") == "retired":
        print(f"\n  Nenhuma caixa conectada {address.strip().lower()}. Veja: sellbird inboxes list\n")
        return None
    return row


async def _find_campaign(store: MailboxStore, ref: str) -> str | None:
    rows = await store._rows("SELECT id, name FROM campaigns WHERE id = ? OR name = ?",
                             (ref, ref))
    if len(rows) != 1:
        print(f"\n  {'Nenhuma' if not rows else 'Mais de uma'} campanha corresponde a {ref!r}. "
              "Use o id dela (sellbird status lista as campanhas).\n")
        return None
    return rows[0]["id"]


async def run(args, store: MailboxStore, secrets: SecretStore, config, env) -> int:
    action = args.inboxes_action or "list"
    if action == "list":
        await print_inbox_list(store, config, env)
        return 0
    if action == "connect":
        return await connect_flow(args, store, secrets, config, env)
    if action == "use":
        campaign_id = await _find_campaign(store, args.campaign)
        if campaign_id is None:
            return 1
        ids = []
        for address in args.addresses:
            if address.strip().lower() == MAIN_NAME:
                ids.append(MAIN)
                continue
            row = await _find(store, address)
            if row is None:
                return 1
            ids.append(row["id"])
        await store.set_campaign_pool(campaign_id, ids)
        print("\n  " + ("Esta campanha envia de todas as caixas." if not ids else
                        f"Esta campanha envia de {len(ids)} caixa(s) apenas.")
              + " Novos tópicos seguem isso; tópicos já iniciados mantêm sua caixa.\n")
        return 0

    row = await _find(store, args.address)
    if row is None:
        return 1
    address = row["address"]
    if action == "test":
        provider = build_provider(row, config=config, env=env, secrets=secrets)
        if provider is None:
            print("\n  ✗ Esta caixa não tem conexão para testar.\n")
            return 1
        return 0 if await _test_and_print(provider) else 1
    if action == "pause":
        await store.set_pause(row["id"], args.reason)
        await store.log_action(action_type="inbox_paused", agent="you",
                               details={"inbox": address, "reason": args.reason})
        print(f"\n  {address} pausada. Seus primeiros e-mails não enviados vão para suas outras caixas; "
              "follow-ups e respostas em tópicos iniciados por ela esperam por ela.\n")
    elif action == "resume":
        await store.set_pause(row["id"], "")
        await store.log_action(action_type="inbox_resumed", agent="you",
                               details={"inbox": address})
        print(f"\n  {address} volta a enviar.\n")
    elif action == "cap":
        await store.set_cap(row["id"], args.cap)
        await store.log_action(action_type="inbox_cap", agent="you",
                               details={"inbox": address, "cap": args.cap})
        print(f"\n  {address}: " + (f"até {args.cap} e-mails frios por dia." if args.cap else
                                     "de volta ao limite diário padrão e sua rampa de aquecimento.") + "\n")
    elif action == "name":
        await store.set_display_name(row["id"], args.name)
        print(f"\n  {address} envia como {args.name.strip() or config.persona.name}.\n")
    elif action == "remove":
        await store.retire(row["id"])
        await store.log_action(action_type="inbox_removed", agent="you",
                               details={"inbox": address})
        print(f"\n  {address} removida. Seus primeiros e-mails não enviados vão para suas outras caixas; "
              "follow-ups em tópicos iniciados por ela são cancelados. O login dela continua em "
              "seu keychain (serviço 'sellbird'); apague-o lá se quiser.\n")
    return 0


def cmd_inboxes(args) -> None:
    from sellbird.config import load_config, load_env
    from sellbird.state import StateManager

    config, env = load_config(), load_env()

    async def _run() -> int:
        state = StateManager()
        await state.init_db()
        return await run(args, MailboxStore(db_path=state.db_path), SecretStore(), config, env)

    sys.exit(asyncio.run(_run()))
