import httpClient from "@/utils/httpClient";

const host = "/api/devops";

export function registerUser(data){
  return httpClient({
    url: `${host}/auth/register`,
    method: 'post',
    data
  })
}

export function loginUser(data){
  return httpClient({
    url: `${host}/auth/login`,
    method: 'post',
    data
  })
}