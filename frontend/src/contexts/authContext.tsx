//Author: Oscar Reina

import { createContext, ReactNode, useState, useEffect, Dispatch, SetStateAction } from "react";

interface AuthContextProps {
  children: ReactNode;
}

interface UserRetrieved {
  id: string;
  username: string;
  email: string;
  is_superuser: boolean;
}

interface AuthContextValue {
  user: UserRetrieved | null;
  setUser: Dispatch<SetStateAction<UserRetrieved | null>>;
  login: (userData: UserRetrieved) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<AuthContextProps> = ({ children }) => {
  const [user, setUser] = useState<UserRetrieved | null>(() => {
    const storedUser = localStorage.getItem("user");
    return storedUser ? JSON.parse(storedUser) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  const login = (userData: UserRetrieved) => {
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
  };

  const contextValue: AuthContextValue = {
    user,
    setUser,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};
