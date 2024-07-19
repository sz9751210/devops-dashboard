// src/api/settings.js

import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function fetchSettings() {
  return httpClient({
    url: `${host}/settings`,
    method: "get",
  });
}

export function addSetting(data) {
  return httpClient({
    url: `${host}/settings`,
    method: "post",
    data,
  });
}

export function updateSetting(id, data) {
  return httpClient({
    url: `${host}/settings/${id}`,
    method: "put",
    data,
  });
}

export function deleteSetting(id) {
  return httpClient({
    url: `${host}/settings/${id}`,
    method: "delete",
  });
}
