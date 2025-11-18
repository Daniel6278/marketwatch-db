
class User {
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
  user: User | null;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

export const UserContext = createContext<UserContextType | null>(null);

// 2. Create a Provider Component
import type { ReactNode } from 'react';

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null); // Example global state

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};