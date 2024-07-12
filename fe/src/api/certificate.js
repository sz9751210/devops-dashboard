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
    params: { domain }
  });
}
