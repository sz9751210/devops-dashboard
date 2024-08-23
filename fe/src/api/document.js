import httpClient from "@/utils/httpClient";

const host = "/api/devops";

// 文件 API
export function fetchDocuments(folder_id) {
  return httpClient({
    url: `${host}/documents?folder_id=${folder_id}`,
    method: "get",
  });
}

export function fetchDocumentDetail(id) {
  return httpClient({
    url: `${host}/documents/${id}`,
    method: "get",
    timeout: 30000
  });
}

export function createDocument(data) {
  return httpClient({
    url: `${host}/documents`,
    method: "post",
    data,
    timeout: 30000
  });
}

export function updateDocument(id, data) {
  return httpClient({
    url: `${host}/documents/${id}`,
    method: "put",
    data,
    timeout: 30000
  });
}

export function deleteDocument(id) {
  return httpClient({
    url: `${host}/documents/${id}`,
    method: "delete",
    timeout: 30000
  });
}

// 目錄 API
export function fetchFolders() {
  return httpClient({
    url: `${host}/folders`,
    method: "get",
  });
}

export function createFolder(data) {
  return httpClient({
    url: `${host}/folders`,
    method: "post",
    data,
  });
}

export function updateFolder(id, data) {
  return httpClient({
    url: `${host}/folders/${id}`,
    method: "put",
    data,
  });
}

export function deleteFolder(id) {
  return httpClient({
    url: `${host}/folders/${id}`,
    method: "delete",
  });
}

export function uploadImage(formData) {
  return httpClient({
    url: `${host}/upload-image`,
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}
