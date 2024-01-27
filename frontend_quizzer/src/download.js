export function useDownloadJSON(json) {
  const jsonStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(json))
  const a = document.createElement('a')
  a.setAttribute("href", jsonStr)
  a.setAttribute("download", "quiz.json")
  a.setAttribute("target", "_blank")
  a.click()
  a.remove()
}
