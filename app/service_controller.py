import subprocess
import asyncio
import os


def start_pm2_process(app_name):
    try:

        save_command = ["pm2", "save"]
        pm2_command = ["pm2", "start", f'/home/sinapse/leitor_termo/{app_name}'+'.py']
        result = subprocess.run(pm2_command, capture_output=True, text=True, check=True)
        save = subprocess.run(save_command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
      
    except subprocess.CalledProcessError as e:
        return e.stderr

    except Exception as e:
        return str(e)
    

def stop_pm2_process(app_name):
    try:
        save_command = ["pm2", "save"]
        pm2_command = ["pm2", "stop", f"/home/sinapse/leitor_termo/{app_name}"+'.py']
        result = subprocess.run(pm2_command, capture_output=True, text=True, check=True)
        save = subprocess.run(save_command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
      
    except subprocess.CalledProcessError as e:
        return e.stderr

    except Exception as e:
        return str(e)


def status_pm2_process(app_name):

    try:
        pm2_command = ['pm2', 'show', f'{app_name}']
        result = subprocess.run(pm2_command, capture_output=True, text=True, check=True)

        return result.stdout
    
    except subprocess.CalledProcessError as e:
        return e.stderr
    except Exception as e:
        return str(e)





async def test_read_temp():
    try:

        pm2_command1 = ['pm2', 'stop', 'task_read_temp']
        pm2_command2 = ['python', '/home/sinapse/leitor_termo/teste.py']
        pm2_command3 = ['pm2', 'restart', 'task_read_temp']
        
        result = subprocess.run(pm2_command1, capture_output=True, text=True, check=True)
        process = await asyncio.create_subprocess_exec(*pm2_command2, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()

        result = subprocess.run(pm2_command3, capture_output=True, text=True, check=True)

        if stderr:
            return stderr.decode().strip()
        else:
            return stdout.decode().strip()
    
    except Exception as e:
        return str(e)

