
import React, { createContext, useContext, useState } from "react";

class Snackbar {
    id: string;
    message: string;
    requestPayload: string | null;
    response: string;
    sql: string | null;

    constructor(message: string, request: string | null, response: string, sql: string | null) {
        this.id = crypto.randomUUID();
        this.message = message;
        this.requestPayload = request;
        this.response = response;
        this.sql = sql;
    }
}
const SNACKBAR_PERSIST_DURATION_MS = 5000;

// 1. Create the Context

interface SnackbarsContextType {
  items: Snackbar[];
  push: (item: Snackbar) => void;
}

export const SnackbarsContext = createContext<SnackbarsContextType | undefined>(undefined);

// 2. Create a Provider Component

export const SnackbarsProvider = ({ children }: { children: React.ReactNode }) => {
    const [items, setItems] = useState<Snackbar[]>([]);
    const removeItem = (id: string) => {
        setItems((prev) => prev.filter((item) => item.id !== id));
    };
    const push = (item: Snackbar) => {
        setItems((prev) => [...prev, item]); // ← append to list

        setTimeout(() => {
            removeItem(item.id);
        }, SNACKBAR_PERSIST_DURATION_MS);
    };

  return (
    <SnackbarsContext.Provider value={{ items, push }}>
      {children}
    </SnackbarsContext.Provider>
  );
};