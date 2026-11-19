"""Harvey is now Sellbird.

This package only keeps the old ``harvey`` command and ``python -m harvey``
working for a while after the rename, including for clones that ran
``git pull`` without reinstalling. Everything lives in ``sellbird``.
"""

NOTICE = ("Harvey agora é Sellbird. Rode `pip install -e .` uma vez, depois use `sellbird` "
          "em vez de `harvey`. O comando `harvey` será removido em uma versão futura.")
