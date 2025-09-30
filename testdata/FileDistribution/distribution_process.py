from helpers import strings
from typing import Dict, Any

ftp_distribution_payload = {
    'protocol': 'ftp',
    'accepts_advisories': False,
    'accepts_hd_videos': False,
    'accepts_sd_videos': False,
    'accepts_scripts': True,
    'purge_hours': 0,
    'name': 'testAutoFTP',
    'manual': True,
    'video_script_together': False,
    'legacy_mode': 0,
    'all_user': True,
    'uri': 'dummy_host',
    'username': 'dummy_username',
    'password': 'dummy_password',
    'remote_base_directory': '/testAuto',
    'port': 21,
    'active': False,
    'append_tmp_during_xfer': False,
    'filters': [
        {
            'id': 1,
            'expected_value': ''
        }
    ]
}

ftps_extra_arg = {
    'protocol': 'ftps',
    'name': 'autoTestFTPS',
    'trust_mgr': 'all',
    'data_channel_protection': 'C',
    'implicit': False,
}
sftp_extra_arg = {
    'protocol': 'sftp',
    'name': 'autoTestSFTP',
    'remote_base_directory': '/wneclient/data/QA/sftp/testAuto'
}


ftps_distribution_payload = {**ftp_distribution_payload, **ftps_extra_arg}

smb_distribution_payload: dict[str | Any, str | bool | int | Any] = { #we are giving the details which are supposed to be filled for smb23 process
        'name': 'autoDistSmb13',
        'protocol': 'smb23',
        'manual': True,
        'video_script_together': False,
        'accepts_sd_videos': False,
        'accepts_hd_videos': False,
        'legacy_mode': 0,
        'legacy_video_references': "SDHD",
        'accepts_scripts': True,
        'accepts_advisories': False,
        'all_user': True,
        'status': 1,
        'filters': [
            {
                "id": 1
            }
        ],
        'valid': True,
        'target_directory': "10.99.13.117/share/SMBTestSWonlyUbuntu",
        'purge_hours': 0
}
ftps_distribution_payload = {**ftp_distribution_payload, **ftps_extra_arg} #ftp_distribution_payload and ftps_extra_arg are two dictionaries.
#The ** syntax is used to unpack the contents of these dictionaries and merge them into a new dictionary called tps_distribution_payload.
#If there are overlapping keys between ftp_distribution_payload and ftps_extra_arg, the values from ftps_extra_arg will overwrite the values from ftp_distribution_payload.
sftp_distribution_payload = {**ftp_distribution_payload, **sftp_extra_arg}
sftp_distribution_payload = {k: v for k, v in sftp_distribution_payload.items() if k not in [
    'port', 'active', 'append_tmp_during_xfer']}
existing_name = {'ftp': 'AutoDist9876Ftp',
                 'ftps': 'AutoDist9876Ftps', 'sftp': 'AutoDist9876Sftp'}
distribution_base_directory = {"ftp": '/wneclient/data/QA/ftp/files',
        "ftps": '/wneclient/data/QA/ftps/files', "sftp": '/wneclient/data/QA/sftp'}
create_distribution_test_data = [
    ('ftp', {'name': existing_name['ftp']}, 409, {'error': 'name_exists',
                    'message': f'Distribution process name {existing_name["ftp"]} already exists'}),
    ('ftp', {'name': ''}, 422, {'error': 'empty_name',
                                'message': 'name cannot be null, empty or blank'}),
    ('ftp', {'name': '!@#$%^&'}, 422, {'error': 'name_incorrect',
                                       'message': 'The name fails regex check'}),
    ('ftp', {'name': 'The quick brown fox jumps over lazy dog FTP'}, 200, {}),
    ('ftp', {'name': 'Combien ça coûte FTP'}, 422, {
        'error': 'name_incorrect', 'message': 'The name fails regex check'}),
    ('ftp', {'name': 'اختبار اللغة العربية'}, 422, {
        'error': 'name_incorrect', 'message': 'The name fails regex check'}),
    ('ftp', {'name': strings.random(100)}, 200, {}),
    ('ftp', {'name': strings.random(15), 'remote_base_directory': ''}, 422, {
        'error': 'remote_base_directory_empty', 'message': 'remote base directory cannot be null'}),
    ('ftp', {'name': strings.random(15),
             'remote_base_directory': '/testAutoDistribution'}, 200, {}),
    ('ftp', {'name': strings.random(15), 'uri': ''}, 422, {
        'error': 'uri_empty', 'message': 'uri cannot be null'}),
    ('ftps', {'name': existing_name['ftps']}, 409, {'error': 'name_exists',
                'message': f'Distribution process name {existing_name["ftps"]} already exists'}),
    ('ftps', {'name': ''}, 422, {'error': 'empty_name',
                                 'message': 'name cannot be null, empty or blank'}),
    ('ftps', {'name': '!@#$%^&'}, 422, {'error': 'name_incorrect',
                                        'message': 'The name fails regex check'}),
    ('ftps', {'name': 'The quick brown fox jumps over lazy dog FTPS'}, 200, {}),
    ('ftps', {'name': 'Combien ça coûte FTPS'}, 422, {
        'error': 'name_incorrect', 'message': 'The name fails regex check'}),
    ('ftps', {'name': 'اختبار اللغة البية'}, 422, {
        'error': 'name_incorrect', 'message': 'The name fails regex check'}),
    ('ftps', {'name': strings.random(100)}, 200, {}),
    ('ftps', {'name': strings.random(15), 'remote_base_directory': ''}, 422, {
        'error': 'remote_base_directory_empty', 'message': 'remote base directory cannot be null'}),
    ('ftps', {'name': strings.random(15),
              'remote_base_directory': '/testAutoDistribution'}, 200, {}),
    ('ftps', {'name': strings.random(15), 'uri': ''}, 422, {
        'error': 'uri_empty', 'message': 'uri cannot be null'}),
    ('sftp', {'name': existing_name['sftp']}, 409, {'error': 'name_exists',
            'message': f'Distribution process name {existing_name["sftp"]} already exists'}),
    ('sftp', {'name': ''}, 422, {'error': 'empty_name',
                                 'message': 'name cannot be null, empty or blank'}),
    ('sftp', {'name': '!@#$%^&%'}, 422, {'error': 'name_incorrect',
                                         'message': 'The name fails regex check'}),
    ('sftp', {'name': 'The quick brown fox jumps over lazy dog SFTP'}, 200, {}),
    ('sftp', {'name': 'Combien ça coûte SFTP'}, 422, {
        'error': 'name_incorrect', 'message': 'The name fails regex check'}),
    ('sftp', {'name': 'اختبار للغة العربية'}, 422, {
        'error': 'name_incorrect', 'message': 'The name fails regex check'}),
    ('sftp', {'name': strings.random(100)}, 200, {}),
    ('sftp', {'name': strings.random(15), 'remote_base_directory': ''}, 422, {
        'error': 'remote_base_directory_empty', 'message': 'remote base directory cannot be null'}),
    ('sftp', {'name': strings.random(15),
              'remote_base_directory': '/testAutoDistribution'}, 200, {}),
    ('sftp', {'name': strings.random(15), 'uri': ''}, 422, {
        'error': 'uri_empty', 'message': 'uri cannot be null'}),
]
