import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function addCronjob(cronjob) {
  return httpClient({
    url: `${host}/cronjob`,
    method: "post",
    data: cronjob,
  });
}

export function editCronjob(id, cronjob) {
  return httpClient({
    url: `${host}/cronjob/${id}`,
    method: "put",
    data: cronjob,
  });
}

export function fetchCronjobs() {
  return httpClient({
    url: `${host}/cronjobs`,
    method: "get",
  });
}

export function deleteCronjob(id) {
  return httpClient({
    url: `${host}/cronjob/${id}`,
    method: "delete",
  });
}
