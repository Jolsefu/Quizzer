export function useDateParser(dtString) {
  const dt = new Date(dtString)

  return `${dt.toLocaleDateString()} ${dt.toLocaleTimeString()}`
}
