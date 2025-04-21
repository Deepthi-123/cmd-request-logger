import click
import logging
from cmd_logger.cmdlogger.constants import CMD_TABLE
from cmd_logger.cmdlogger.db_service import DatabaseService, DBConnectionPoolService

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(name)s %(message)s'
)

db_pool = DBConnectionPoolService()
db_service = DatabaseService(db_pool)

@click.command()
@click.option('--cmd', help='The command to be logged')
@click.option('-q', '--quiet', default=False, help='Suppress output')
def cmdlog(cmd, quiet):
    if cmd:
        try:
            db_service.execute_save(CMD_TABLE, cmd=cmd)
            if not quiet:
                click.echo("Command logged successfully.")
        except Exception as e:
            LOGGER.error(f"failed to execute save of cmd {cmd[:15]}...:{e}")


