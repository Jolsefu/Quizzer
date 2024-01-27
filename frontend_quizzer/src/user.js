
/**
 * 
 * User authentication handling
 * 
 */

import { ref } from "vue"

const token = ref(null)
const username = ref(null)

export function useGetToken() {
  return token.value
}

export function useGetUsername() {
  return username.value
}

export function useSetUser(jsonData) {
  if (jsonData.token === token.value) {
    return {error: 'You are already logged in.'}
  }

  username.value = jsonData.user.username
  token.value = jsonData.token

  return {error: false}
}

export function useIsAuthenticated() {
  return token.value !== null ? true : false
}
