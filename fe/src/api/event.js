// src/api/event.js
import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function fetchEvent() {
  return httpClient({
    url: `${host}/event`,
    method: "get",
  });
}

// 可以添加更多的API方法，例如新增事件、更新事件等
export function createEvent(data) {
  return httpClient({
    url: `${host}/event`,
    method: "post",
    data,
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
