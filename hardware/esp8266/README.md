# WebREPL CLI for ESP8266

### Upload a file to your ESP8266:
```bash
python3 webrepl_cli.py -p waterme main.py 10.0.0.105:main.py
```

### Download a file from ESP:
```bash
python3 webrepl_cli.py -p waterme 10.0.0.105:main.py main_backup.py
```

### Soft reboot the board:
```python
import machine
machine.reset()
```

WebREPL must be enabled on the board and the password must be set to match (default: `waterme`).
