import subprocess
import os

def run_command(cmd: str, cwd: str = None) -> dict:
    try:
        res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return {"code": res.returncode, "stdout": res.stdout, "stderr": res.stderr}
    except Exception as e:
        return {"code": -1, "stdout": "", "stderr": str(e)}

def push_to_github(repo_name: str, project_path: str, commit_msg: str = "Automated deploy by Sales OS Agent"):
    """إنشاء ريبو على جيت هاب وعمل بوش للكود"""
    commands = [
        "git init",
        "git branch -M main",
        "git add .",
        f'git commit -m "{commit_msg}"',
        f"gh repo create {repo_name} --public --source=. --remote=origin --push || git push -u origin main"
    ]
    logs = []
    for cmd in commands:
        out = run_command(cmd, cwd=project_path)
        logs.append(f"[{cmd}] -> {out['stdout'] or out['stderr']}")
    return logs

def deploy_to_vercel(project_path: str,def deploy_to_vercel(project_اdef deploy_to_�و�def d�لى def deploy_to_vercel(project_path: str,def deploy_��def dep��def deploy_to_vercel(project_path: str,def deploy_to_vercel(project_اdef deploy_to_depdef deploy_to_vercel(project_path: str,def deploy_to_vercel(project_اdef deploy_t'sdef deploy_to_vercel(projmain:
        domain_cmd = f"npx vercel domains add {domain} --yes"
        d_res = run_command(domain_cmd, cwd=project_path)
        logs.append(f"[Vercel Domain Link] -> {d_res['stdout'] or d_res['stderr']}")
        
    return logs
