from typing import Mapping, Optional


def features() -> Mapping[str, Optional[str]]:
    if not hasattr(features, 'features'):
        setattr(features, 'features', {
            'modstrawpoll': '!strawpoll for mods',
            })
    return getattr(features, 'features')
