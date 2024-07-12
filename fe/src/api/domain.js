import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function fetchDomain() {
  return httpClient({
    url: `${host}/domains`,
    method: "get",
  });
}
