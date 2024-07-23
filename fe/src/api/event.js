// src/api/event.js
import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function fetchEvent() {
  return httpClient({
    url: `${host}/event`,
    method: "get",
  });
}

export function fetchEventDetail(id) {
  return httpClient({
    url: `${host}/event/${id}`,
    method: "get",
  });
}

export function createEvent(data) {
  return httpClient({
    url: `${host}/event`,
    method: "post",
    data,
    timeout: 30000
  });
}

export function updateEvent(id, data) {
  return httpClient({
    url: `${host}/event/${id}`,
    method: "put",
    data,
  });
}

export function deleteEvent(id) {
  return httpClient({
    url: `${host}/event/${id}`,
    method: "delete",
  });
}
