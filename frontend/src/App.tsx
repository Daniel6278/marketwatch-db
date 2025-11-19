import "./App.css"; // Import the CSS file

import { Routes, Route } from "react-router-dom";

import CreateAccount from "./pages/CreateAccount";
import MyAccount from "./pages/MyAccount";
import PriceHistory from "./pages/PriceHistory";
import Tickers from "./pages/Tickers";
import AdminDashboard from "./pages/admin/Dashboard";
import Landing from "./pages/Landing";
import GlobalNavBar from "./components/GlobalNavBar";

import { Button } from "./components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card";

import SignIn from "./components/SignIn";
import Toast from "./components/Toast";

import { useContext, useState } from "react";
import {
  useDevFeedbackDetailsDialog,
  useSignInDialog,
} from "./context/GlobalModalDialogsStatesContext";
import {
  ActionFeedbackToastsContext,
  Feedback,
} from "./context/ActionFeedbackToastsContext";
import { UserContext, FrontendUser } from "./context/ActiveUserContext";
import Modal from "./components/Modal";

function App() {
  const activeUserContext = useContext(UserContext);
  const actionFeedbackToastsContext = useContext(ActionFeedbackToastsContext);

  const signInDialog = useSignInDialog();
  const devFeedbackDetailsDialog = useDevFeedbackDetailsDialog();

  async function login(email: string, password: string) {
    apiCall(
      activeUserContext,
      actionFeedbackToastsContext,
      {
        endpoint: "signin",
        method: "POST",
        params: {
          email,
          password,
        },
      },
      ({ credentials }: { credentials: string }) => {
        activeUserContext?.setUser(
          new FrontendUser(
            credentials,
            activeUserContext,
            actionFeedbackToastsContext
          )
        );
      },
      true,
      {
        successFeedbackMessage: "Login successful.",
        failureFeedbackMessage: "Login failed.",
      }
    );
  }

  const [expandedFeedbackItem, setExpandedFeedbackItem] = useState<Feedback>();

  return (
    <>
      <div>
        <GlobalNavBar />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/register" element={<CreateAccount />} />
          <Route path="/me" element={<MyAccount />} />
          <Route
            path="/pricehistory/:tickerSymbol"
            element={<PriceHistory />}
          />
          <Route path="/tickers" element={<Tickers />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </div>

      {(() => {
        if (signInDialog?.dialogState.isOpen) {
          console.log("App.tsx : Dialog Is Open");
          return (
            <Modal onCloseButtonClick={() => signInDialog.closeDialog()}>
              <SignIn onLogin={login} />
            </Modal>
          );
        }
        return undefined;
      })()}

      <div
        className="fixed z-[1000]"
        style={{ width: "50rem", bottom: 0, left: 0 }}
      >
        {actionFeedbackToastsContext.items.map((feedbackItem: Feedback) => (
          <Toast
            message={feedbackItem.message}
            variant={feedbackItem.variant}
            onOpenDetails={() => {
              devFeedbackDetailsDialog.openDialog();
              setExpandedFeedbackItem(feedbackItem);
            }}
          ></Toast>
        ))}
      </div>

      {(() => {
        if (devFeedbackDetailsDialog?.dialogState.isOpen) {
          console.log("App.tsx : Feedback Dialog Is Open");
          return (
            <Modal
              onCloseButtonClick={() => devFeedbackDetailsDialog.closeDialog()}
            >
              placeholder
            </Modal>
          );
        }
        return undefined;
      })()}
    </>
  );
}

export default App;

class AuthError extends Error {
  constructor(message) {
    super(message);
    this.name = "AuthError";
  }
}
class PermissionError extends Error {
  constructor(message) {
    super(message);
    this.name = "PermissionError";
  }
}
class ServerError extends Error {
  constructor(message) {
    super(message);
    this.name = "ServerError";
  }
}
class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = "NetworkError";
  }
}

export async function apiCall(
  activeUserContext,
  actionFeedbackToastsContext,
  {
    endpoint,
    method,
    params,
  }: {
    endpoint: string;
    method: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
    params?: object;
  },
  callback: Function,
  doShowFeedbackToast: boolean,
  {
    successFeedbackMessage,
    failureFeedbackMessage,
  }: { successFeedbackMessage?: string; failureFeedbackMessage?: string } = {}
) {
  const API_ORIGIN = "https://specific-brande-data-group-585a3e34.koyeb.app";

  let url = `${API_ORIGIN}/${endpoint}`;
  const headers = {};
  if (activeUserContext.user) {
    headers["Authorization"] = activeUserContext.user.httpCredentials;
  }
  const requestOptions = {
    method,
    headers,
  };
  const hasParams: boolean = params && Object.entries(params).length > 0;
  const paramsStringified = JSON.stringify(params);
  if (hasParams && ["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
    headers["Content-Type"] = "application/json";
    requestOptions["body"] = paramsStringified;
  } else if (hasParams && method === "GET") {
    const strParams: Record<string, string> = Object.fromEntries(
      Object.entries(params).map(([k, v]) => [k.toString(), v.toString()])
    );
    const urlSearchParams = new URLSearchParams(strParams);
    url += `?${urlSearchParams.toString()}`;
  }

  let responseStatusCode = undefined;
  let responseText = undefined;
  let responseJson = undefined;
  try {
    const response = await fetch(url, requestOptions);
    responseStatusCode = response.status;
    const responseClone = response.clone();
    responseText = await response.text();
    if (!response.ok) {
      if (responseStatusCode === 401) {
        // if current stored user credentials are unauthorized, delete them, so user can sign in again
        activeUserContext.user.setUser(null);
      }
      throw new ServerError(responseText);
    }
    responseJson = await responseClone.json();
    callback(responseJson);

    if (doShowFeedbackToast) {
      if (responseJson.hasOwnProperty("sql")) {
        actionFeedbackToastsContext.push(
          new Feedback(
            "SUCCESS",
            successFeedbackMessage,
            url,
            paramsStringified,
            responseStatusCode,
            JSON.stringify(
              Object.fromEntries(
                Object.entries(responseJson).filter(([k, v]) => k !== "sql")
              )
            ),
            responseJson.sql
          )
        );
      } else {
        actionFeedbackToastsContext.push(
          new Feedback(
            "SUCCESS",
            successFeedbackMessage,
            url,
            paramsStringified,
            responseStatusCode,
            responseText
          )
        );
      }
    }
  } catch (error) {
    if (doShowFeedbackToast) {
      actionFeedbackToastsContext.push(
        new Feedback(
          "FAIL",
          failureFeedbackMessage,
          url,
          paramsStringified,
          responseStatusCode,
          responseText
        )
      );
    }

    if (error instanceof AuthError) {
      console.error(`AuthError: ${error.message}`);
    } else if (error instanceof PermissionError) {
      console.error(`PermissionError: ${error.message}`);
    } else if (error instanceof ServerError) {
      console.error(`ServerError: ${error.message}`);
    } else {
      // If it's an unknown error type, re-throw it or handle as a generic error
      console.error("Error: ", error);
    }
  }
}

export type MissingValueStatus = "PENDING" | null;
export const PENDING: MissingValueStatus = "PENDING";
