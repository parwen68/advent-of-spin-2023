import { HandleRequest, HttpRequest, HttpResponse, Kv } from "@fermyon/spin-sdk"
export const handleRequest: HandleRequest = async function (request: HttpRequest): Promise<HttpResponse> {
  const store = Kv.openDefault()

  console.log(request)

  if (request.method === "GET") {
    const key = request.uri.split("?")

    if (key.length > 1) {
      const data = store.getJson(key[1])
      if (data) {
        return {
          status: 200,
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ value: data })
        }
      } else {
        return { status: 404 }
      }
    }
    return {
      status: 400,
    }
  } else if (request.method === "POST") {

    const key = request.uri.split("?")

    if (key.length > 1) {
      if (request.body) {
        let data = JSON.parse(new TextDecoder().decode(request.body))
        if (data && data.value) {
          store.setJson(key[1], data.value)
          return {
            status: 201,
          }
        }
      }
    }
    return {
      status: 400,
    }
  }

  return {
    status: 405,
    headers: { "content-type": "text/plain" },
    body: "Method Not Allowed"
  }
}
