import React, { createContext, useContext, useState } from "react";

export class Feedback {
  _id: string;

  variant: "SUCCESS" | "FAIL";
  message: string;
  requestUrl: string;
  requestParams: string | string;
  responseStatus: number | string | undefined;
  responseBody: string | undefined;
  sql: string | undefined;

  constructor(
    variant: "SUCCESS" | "FAIL",
    message,
    requestUrl,
    requestParams,
    responseStatus,
    responseBody,
    sql?
  ) {
    this._id = crypto.randomUUID();

    this.variant = variant;
    this.message = message;
    this.requestUrl = requestUrl;
    this.requestParams = requestParams;
    this.responseStatus = responseStatus;
    this.responseBody = responseBody;
    this.sql = sql;
  }
}
const TOAST_PERSIST_DURATION_MS = 5000;

// 1. Create the Context

interface ActionFeedbackToastsContextType {
  items: Feedback[];
  push: (item: Feedback) => void;
}

export const ActionFeedbackToastsContext = createContext<
  ActionFeedbackToastsContextType | undefined
>(undefined);

// 2. Create a Provider Component

export const ActionFeedbackToastsProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [items, setItems] = useState<Feedback[]>([]);
  const removeItem = (id: string) => {
    setItems((prev) => prev.filter((item) => item._id !== id));
  };
  const push = (item: Feedback) => {
    setItems((prev) => [...prev, item]); // ← append to list

    setTimeout(() => {
      removeItem(item._id);
    }, TOAST_PERSIST_DURATION_MS);
  };

  return (
    <ActionFeedbackToastsContext.Provider value={{ items, push }}>
      {children}
    </ActionFeedbackToastsContext.Provider>
  );
};
