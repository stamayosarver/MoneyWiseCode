import { useAuth0 } from "@auth0/auth0-react"
import { KeyRoundIcon, LogInIcon, LogOutIcon, WalletIcon } from "lucide-react"
import { useCallback, useEffect, useState } from "react"
import { PlaidLinkOnSuccess, usePlaidLink } from "react-plaid-link"
import { Button } from "./components/ui/button"
import config from "./config"

export default () => {
  const { isAuthenticated, logout } = useAuth0()
  const component = isAuthenticated ? <Authenticated /> : <Unauthenticated />

  return (
    <div className="h-screen flex items-center justify-center bg-zinc-50">
      <div className="flex flex-col gap-4 max-w-lg w-full border p-6 rounded shadow bg-white">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1">
            <WalletIcon className="h-7 w-7 text-emerald-800" />
            <span
              className="font-semibold text-xl tracking-tighter"
            >
              MoneyWise
            </span>
          </div>
          { isAuthenticated && (
            <Button
              size="sm"
              variant="ghost"
              className="text-red-500 hover:text-red-500/90 flex items-center gap-2 text-xs"
              onClick={() => logout()}
            >
              <LogOutIcon className="h-4 w-4" />
              Sign Out
            </Button>
          )}
        </div>
        { component }
      </div>
    </div>
  )
}

const Unauthenticated = () => {
  const { loginWithPopup } = useAuth0()

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col">
        <h2
          className="text-lg font-medium"
        >
          It appears you are not signed in
        </h2>
        <p
          className="text-zinc-700"
        >
          Please sign in or create an account to continue
        </p>
      </div>
      <Button
        size="lg"
        className="bg-emerald-800 hover:bg-emerald-800/90 rounded-full text-md flex items-center gap-2"
        onClick={() => loginWithPopup()}
      >
        <LogInIcon className="h-5 w-5" />
        Sign In
      </Button>
    </div>
  )
}

const Authenticated = () => {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col">
        <h2
          className="text-lg font-medium"
        >
          Please connect your financial accounts below
        </h2>
        <p
          className="text-zinc-700"
        >
          Once you have connected your accounts, you will receive an email from your assistant
        </p>
      </div>
      <ConnectAccountButton />
    </div>
  )
}

const ConnectAccountButton = () => {
  const { user } = useAuth0()
  const [token, setToken] = useState<string | null>(null)
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    (async () => {
      const payload = { user: user?.sub }

      const response = await fetch(config.api.baseUrl + "/plaid/link-token", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      const { token } = await response.json()

      setToken(token)
    })()
  }, [])

  const onSuccess = useCallback<PlaidLinkOnSuccess>(async (publicToken, _) => {
    const payload = {
      user: user?.sub,
      email: user?.email,
      public_token: publicToken,
    }

    await fetch(
      config.api.baseUrl + "/plaid/access-token",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }
    )
    
    setConnected(true)
  }, [])

  const { open, ready } = usePlaidLink({
    token,
    onSuccess
  })

  if (connected) {
    return (
      <h2>
        Your accounts have been connected. You will receive an email shortly.
      </h2>
    )
  }

  return (
    <Button
      disabled={!ready}
      size="lg"
      className="bg-emerald-800 hover:bg-emerald-800/90 rounded-full text-md flex items-center gap-2"
      onClick={() => open()!}
    >
      <KeyRoundIcon className="h-5 w-5" />
      Connect Accounts
    </Button>
  )
}