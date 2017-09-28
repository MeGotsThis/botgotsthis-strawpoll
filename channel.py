import json
import re
from datetime import datetime, timedelta  # noqa: F401
from typing import Any, Dict, Match, List  # noqa: F401

import aiohttp

import bot
from lib.data import ChatCommandArgs
from lib.helper.chat import min_args, permission, permission_feature
from lib.helper import parser


@permission('moderator')
async def logLastMessage(args: ChatCommandArgs) -> bool:
    m: Match[str]
    m = re.search(r'(?:https?://)strawpoll.me/\d+', str(args.message))
    if 'mainStrawPoll' in args.chat.sessionData:
        if (args.chat.sessionData['mainStrawPoll']
                and not args.permissions.broadcaster):
            cacheStrawPoll: datetime
            cacheStrawPoll = args.chat.sessionData['cacheStrawPoll']
            delta: timedelta = args.timestamp - cacheStrawPoll
            if delta <= timedelta(seconds=60):
                m = None
    if m is not None:
        args.chat.sessionData['lastStrawPoll'] = m.group(0)
        broadcaster: bool = args.permissions.broadcaster
        args.chat.sessionData['mainStrawPoll'] = broadcaster
        args.chat.sessionData['cacheStrawPoll'] = args.timestamp
    return False


@min_args(2)
@permission_feature(('broadcaster', None), ('moderator', 'modstrawpoll'))
async def commandStrawPoll(args: ChatCommandArgs) -> bool:
    if (not args.permissions.broadcaster
            and 'strawpoll' in args.chat.sessionData):
        since: timedelta = args.timestamp - args.chat.sessionData['strawpoll']
        if since < timedelta(seconds=60):
            return False

    parts: List[str] = parser.parseArguments(args.message[1:])

    if len(parts) == 0:
        args.chat.send('You need to provide a title for the poll with 2 or '
                       'more options')
        return False
    if len(parts) < 3:
        args.chat.send('You need to provide 2 or more options for the poll')
        return False

    args.chat.sessionData['strawpoll'] = args.timestamp

    params: Dict[str, Any] = {
        'title': parts[0],
        'options': [],
        }
    i: int
    for i in range(1, len(parts)):
        params['options'].append(parts[i])

    headers = {
        'User-Agent': 'MeGotsThis/BotGotsThis',
        }
    url: str = 'https://www.strawpoll.me/api/v2/polls'
    session: aiohttp.ClientSession
    response: aiohttp.ClientResponse
    async with aiohttp.ClientSession(raise_for_status=True) as session, \
            session.post(url,
                         data=json.dumps(params).encode(),
                         headers=headers,
                         timeout=bot.config.httpTimeout) as response:
        responseJson: Dict[str, Any] = await response.json()
        poll: str = f'''http://strawpoll.me/{responseJson['id']}'''
        args.chat.send(poll)

    args.chat.sessionData['lastStrawPoll'] = poll
    args.chat.sessionData['mainStrawPoll'] = args.permissions.broadcaster
    args.chat.sessionData['cacheStrawPoll'] = args.timestamp

    return True


async def commandLastPoll(args: ChatCommandArgs) -> bool:
    if 'lastStrawPoll' in args.chat.sessionData:
        args.chat.send(args.chat.sessionData['lastStrawPoll'])
    else:
        args.chat.send('There was no straw poll posted')
    return True
