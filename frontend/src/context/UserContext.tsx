
export class UserIdentifier {
    userId: string;
    httpCredentials: string;

    constructor(userId: string, httpCredentials: string) {
        this.userId = userId;
        this.httpCredentials = httpCredentials;
    }
}

// 1. Create the Context
import { createContext, useState } from 'react';

interface UserContextType {
  user: UserIdentifier | null;
  setUser: React.Dispatch<React.SetStateAction<UserIdentifier | null>>;
}

export const UserContext = createContext<UserContextType | null>(null);

// 2. Create a Provider Component
import type { ReactNode } from 'react';

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserIdentifier | null>(null); // Example global state

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};