# Philips Hue Zabbix Template

## Installation

### Dependencies

Install zhue from pypi: `$ pip install zhue`

### Zabbix files
- Copy `zabbix_hue.py` to `/etc/zabbix/bin`: `cp zabbix_hue.py /etc/zabbix/bin/zabbix_hue`
- Make it executable: `chmod +x /etc/zabbix/bin/zabbix_hue`
- Import the zabbix-agent config:
`cp hue.conf /etc/zabbix/zabbix_agentd.conf.d`
- Import `template_philips_hue.xml` on your Zabbix server
