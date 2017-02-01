import os
import logging
import tempfile
import yaml
from skybeard.beards import BeardChatHandler, BeardDBTable
from skybeard.decorators import onerror
from skybeard.predicates import Filters
try:
    from .report import generate_report
except Exception as e:
    print(e)
    raise(e)

curr_path = os.path.dirname(__file__)
logger = logging.getLogger(__name__)

class DailyReport(BeardChatHandler):
    __commands__ = [
            ('myreport', 'send_new_report', 'generates and sends a new daily report'),
            ('newdaily', 'new_reportee', 'configure your daily report'),
            (Filters.document, 'new_options_file', 'new opts file sent'),
            ]
    
    __userhelp__ = """Generates and sends a daily report to  the user. Includes weather, 
    news feeds and UK rail information"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("Creating BeardDBTable.")
        self.report_table = BeardDBTable(self, 'reportees')
    
    async def send_new_report(self, msg):
        with self.report_table as table:
            user_opts = table.find_one(uid=msg['from']['id'])
            if not user_opts:
                await self.sender.sendMessage("I don't have you on file. If you\
                want a daily report, send /newdaily")
                return
            else:
                user_opts['feeds'] = eval(user_opts['feeds'])
                try:
                    response = generate_report(user_opts)
                    await self.sender.sendMessage(response['url'])
                except KeyError as e:
                    logger.error(e)
                    await self.sender.sendMessage('Sorry there was some trouble generating \
                    your report. Please try /myreport again')

    @onerror
    async def new_reportee(self, msg):
        await self.sender.sendDocument((
                'dr_opts.yml', 
                open(os.path.join(curr_path, 'dr_opts.yml'),'rb')))
        txt = """
        Please modify these options for yourself, 
        and send them back to be when you're done.
        Do not change the file name."""
        await self.sender.sendMessage(txt)

    @onerror
    async def new_options_file(self, msg):
        doc = msg['document']
        if doc['file_name'] !='dr_opts.yml':
            return
        else:
            with tempfile.NamedTemporaryFile(suffix=".yml") as opts_file:
                await self._bot.download_file(doc['file_id'], opts_file.file)
                new_opts = yaml.load(open(opts_file.name, 'r'))
                uid = msg['from']['id']
                user = msg['from']['first_name']
                new_opts.update(dict(
                    uid = uid,
                    user = user,
                    enabled = True))
                new_opts['feeds'] = str(new_opts['feeds'])
                with self.report_table as table:
                    dupe_check = table.find_one(uid=uid)
                    if dupe_check:
                        table.update(new_opts, ['uid'])
                    else:
                        table.insert(new_opts)
                    await self.sender.sendMessage('New report options added!')

