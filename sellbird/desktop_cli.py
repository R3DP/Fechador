"""Desktop commands: `sellbird autostart install|uninstall|status`.

The login item starts the tray (`sellbird tray`) when the user logs in. The
logic lives in sellbird.desktop.login_item; this only parses and prints.
Exceptions print their message and exit 1, with no traceback.
"""

import subprocess
import sys


def register_desktop_commands(subparsers) -> None:
    sub = subparsers.add_parser("autostart", help="Iniciar a bandeja do Sellbird quando você fizer login")
    sub.add_argument("autostart_action", choices=["install", "uninstall", "status"])
    sub.add_argument("--port", type=int, default=None,
                     help="Porta do painel que a bandeja usa (padrão: a padrão da bandeja)")
    sub.set_defaults(func=cmd_autostart)


def cmd_autostart(args, *, platform=None, runner=subprocess.run, env=None, home=None):
    from sellbird.desktop import login_item as li

    common = dict(platform=platform, runner=runner, env=env, home=home)
    try:
        if args.autostart_action == "install":
            print(f"  {li.install(port=args.port, **common).message}")
        elif args.autostart_action == "uninstall":
            print(f"  {li.uninstall(**common).message}")
        else:
            state = li.status(**common)
            if not state["installed"]:
                print("  O início automático no login está desligado.")
            elif state["ours"]:
                print(f"  O início automático no login está ligado ({state['path']}).")
            else:
                print(f"  O início automático no login está desligado. {state['path']} existe mas não foi "
                      "criado pelo Sellbird.")
    except (li.UnsupportedPlatform, li.ForeignLoginItem, li.LoginItemFailed) as e:
        print(f"  {e}", file=sys.stderr)
        sys.exit(1)


# ── `sellbird tray` ──

def register(subparsers) -> None:
    sub = subparsers.add_parser("tray", help="Ícone na barra de menu: iniciar, parar e abrir o Sellbird")
    sub.add_argument("--status", action="store_true",
                     help="Imprimir se está rodando e o próximo passo de configuração, e sair")
    sub.add_argument("--port", type=int, default=None,
                     help="Porta do painel (padrão: a última informada, senão 5555)")
    sub.set_defaults(func=cmd_tray)


def cmd_tray(args, *, data_dir=None, transport=None, autostart=None):
    """Show the tray icon, or with --status print two lines. Neither prints
    a URL or a token. No tray on this platform: one stderr line, exit 0 (the
    login item relaunches only after a failure)."""
    import logging
    from pathlib import Path

    from sellbird.desktop import tray
    from sellbird.paths import PROJECT_ROOT

    data_dir = Path(data_dir) if data_dir is not None else PROJECT_ROOT / "data"
    if args.port is not None and not 1 <= args.port <= 65535:
        print(f"  Porta inválida: {args.port}. Deve ser entre 1 e 65535.", file=sys.stderr)
        sys.exit(2)
    port = tray.resolve_port(data_dir, args.port)
    if args.status:
        status = tray.TrayController(data_dir, port=port, transport=transport).status()
        print(f"  Sellbird: {tray.state_label(status)}")
        if status.error:
            print(f"  {status.error}")
        elif status.dashboard != "running":
            print("  Inicie com `sellbird tray` ou `sellbird dashboard`.")
        elif status.sending_paused:
            print(f"  O envio está pausado: {status.sending_paused}")
        return
    if args.port is not None:
        tray.remember_port(data_dir, args.port)
    from sellbird.logsafety import RedactSecrets
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    handler.addFilter(RedactSecrets())
    tray_logger = logging.getLogger("sellbird.tray")
    tray_logger.addHandler(handler)
    tray_logger.setLevel(logging.INFO)
    try:
        tray.run_tray(data_dir, port=port,
                      controller=tray.TrayController(data_dir, port=port, transport=transport),
                      autostart=autostart)
    except tray.TrayUnavailable as e:
        print(f"  {e}", file=sys.stderr)
    finally:
        tray_logger.removeHandler(handler)
