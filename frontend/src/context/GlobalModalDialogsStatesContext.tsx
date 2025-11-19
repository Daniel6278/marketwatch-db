import React, { createContext, useState, useContext } from "react";

type DialogStateManagerType = {
  dialogState: {
    isOpen: boolean;
  };
  openDialog: Function;
  closeDialog: Function;
};

interface GlobalModalDialogStateContextType {
  signIn: DialogStateManagerType;
  addRemoveTickerFromPortfolios: DialogStateManagerType;
  runIndicator: DialogStateManagerType;
  signOut: DialogStateManagerType;
}

const GlobalModalDialogStateContext = createContext<
  GlobalModalDialogStateContextType | undefined
>(undefined);

export const GlobalModalDialogsStatesProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  // TODO : this gets inefficient as more dialogs are added because all children re-render whenever ANY dialog’s state changes
  const contextVal: GlobalModalDialogStateContextType = {
    signIn: null,
    addRemoveTickerFromPortfolios: null,
    runIndicator: null,
    signOut: null,
  };
  for (let dialogName of Object.keys(contextVal)) {
    const [dialogState, setDialogState] = useState({
      isOpen: false,
    });
    const openDialog = () => {
      console.log("open dialog");
      setDialogState({ isOpen: true });
    };
    const closeDialog = () => {
      console.log("close dialog");
      setDialogState({ isOpen: false });
    };
    contextVal[dialogName] = {
      dialogState,
      openDialog,
      closeDialog,
    };
  }

  return (
    <GlobalModalDialogStateContext.Provider value={contextVal}>
      {children}
    </GlobalModalDialogStateContext.Provider>
  );
};

export const useSignInDialog = () => {
  const { signIn } = useContext(GlobalModalDialogStateContext);
  return signIn;
};
