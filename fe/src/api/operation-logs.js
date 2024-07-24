import httpClient from "@/utils/httpClient";

export function fetchOperationLogs(page, pageSize) {
  return httpClient({
    url: `/api/devops/operation_logs`,
    method: "get",
    params: { page, pageSize },
  });
}