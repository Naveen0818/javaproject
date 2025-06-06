import requests

PRISMA_API = "https://your-prisma-console/api/v1"
USERNAME = "your-username"
PASSWORD = "your-password"

def get_token():
    resp = requests.post(f"{PRISMA_API}/authenticate", json={
        "username": USERNAME,
        "password": PASSWORD
    })
    return resp.json()["token"]

def get_images(token, namespace=None):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{PRISMA_API}/images"
    if namespace:
        url += f"?collections={namespace}"
    resp = requests.get(url, headers=headers)
    return resp.json()

def get_vulnerabilities(image_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{PRISMA_API}/images/{image_id}/vulnerabilities"
    resp = requests.get(url, headers=headers)
    return resp.json()

if __name__ == "__main__":
    token = get_token()
    images = get_images(token, namespace="finance")
    for image in images:
        print(f"Image: {image['repoDigests'][0]}")
        vulns = get_vulnerabilities(image["_id"], token)
        for v in vulns:
            print(f" - {v['cve']}: {v['severity']} ({v['packageName']} - {v['packageVersion']})")
