import server.requestHandler

import subprocess
import threading

def launch_replay(gameId, key):
    # PowerShell script as a multi-line string
    powershell_script = '''
    $gamePath = "C:\\Riot Games\\League of Legends\\Game"
    $radsReleasesPath = "C:\\Riot Games\\League of Legends\\RADS\\solutions\\lol_game_client_sln\\releases"

    if (Test-Path $gamePath) {
        Set-Location $gamePath
    } else {
        # Navigate to the releases directory and find the latest version
        Set-Location $radsReleasesPath
        $latestRelease = Get-ChildItem -Directory | Sort-Object Name -Descending | Select-Object -First 1
        Set-Location "$($latestRelease.FullName)\\deploy"
    }

    $env:riot_launched = "true"

    & ".\\League of Legends.exe" `
        "spectator 127.0.0.1:8000 ''' + key + ' ' + gameId + ''' EUW1" `
        "-UseRads" `
        "-GameBaseDir=.."
    '''
    # Execute the PowerShell script
    try:
        result = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True,
            check=True  # Raise an error if the script fails
        )
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)

def launch_replay_n_serv(key, gameId):
    thread = threading.Thread(target = launch_replay, args=(gameId, key))
    thread.start()
    
    server.requestHandler.run()

if __name__ == "__main__":
    launch_replay_n_serv("sf1/Hv/6FHX42EgerviqhWNDdUd1EMP8", "7234213218")