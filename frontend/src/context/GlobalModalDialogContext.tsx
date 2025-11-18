
import React, { createContext, useState, useContext } from 'react';

interface GlobalModalDialogContextType {
  dialogState: {
    isOpen: boolean
  },
  openDialog: Function,
  closeDialog: Function,
}

export const GlobalModalDialogContext = createContext<GlobalModalDialogContextType|undefined>(undefined);

export const GlobalModalDialogProvider = ({ children }: { children: React.ReactNode }) => {
    const [dialogState, setDialogState] = useState({
        isOpen: false
    });

    const openDialog = () => {
        setDialogState({ isOpen: true });
    };

    const closeDialog = () => {
        setDialogState({ isOpen: false });
    };

    return (
    <GlobalModalDialogContext.Provider value={{ dialogState, openDialog, closeDialog }}>
        {children}
    </GlobalModalDialogContext.Provider>
    );
};