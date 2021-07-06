import subprocess


def check_appearance():
    """Checks DARK/LIGHT mode of macos."""
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    return "dark" if bool(p.communicate()[0]) else "light"


config = dict(
    executable_path="/System/Volumes/Data/Applications/Safari Technology Preview.app/Contents/MacOS/safaridriver",
    desired_capabilities={
        "browserName": "Safari Technology Preview",
        "version": "",
        "platform": "MAC",
    },
)
