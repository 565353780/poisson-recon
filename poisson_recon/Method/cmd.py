from subprocess import Popen, PIPE


def runCMD(cmd: str) -> bool:
    subp = Popen(
        cmd,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        encoding="utf-8",
    )
    subp.wait()

    return subp.poll() == 0

    if subp.poll() == 0:
        print(subp.communicate()[1])

    return False
