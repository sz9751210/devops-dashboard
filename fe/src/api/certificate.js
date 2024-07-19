import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function fetchDomain() {
  return httpClient({
    url: `${host}/certificate/domains`,
    method: "get",
  });
}

export function fetchCertificate(domain) {
  return httpClient({
    url: `${host}/certificate/check`,
    method: "get",
    params: { domain },
  });
}

export function updateDomainStatus(data) {
  return httpClient({
    url: `${host}/certificate/domain-status`,
    method: "put",
    data,
  });
}

export function syncCloudflareRecords() {
  return httpClient({
    url: `${host}/certificate/sync-cloudflare`,
    method: "post",
    timeout: 3000000
  });
}

export function checkSubdomains() {
  return httpClient({
    url: `${host}/certificate/check-subdomains`,
    method: "post",
    timeout: 300000
  });
}
