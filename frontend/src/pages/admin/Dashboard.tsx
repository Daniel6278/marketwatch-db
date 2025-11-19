import AdminSignIn from "@/components/AdminSignIn";
import { useContext } from "react";
import { apiCall } from "@/App";

import { UserContext, FrontendUser } from "@/context/ActiveUserContext";
import { ActionFeedbackToastsContext } from "@/context/ActionFeedbackToastsContext";

function AdminDashboard() {
  const activeUserContext = useContext(UserContext);
  const actionFeedbackToastsContext = useContext(ActionFeedbackToastsContext);

  async function login(username: string, password: string) {
    apiCall(activeUserContext, actionFeedbackToastsContext, {
      endpoint: 'admin/signin',
      method: 'POST',
      params: {
            username,
            password,
          },
    }, (credentials) => {
        activeUserContext?.setUser(new FrontendUser(credentials, activeUserContext, actionFeedbackToastsContext));
    }, true, {
      successFeedbackMessage: "Authenticated as admin.",
      failureFeedbackMessage: "Failed to sign in as admin.",
    });
  }

  if (!activeUserContext.user) {
    return (
      <div className="max-w-md mx-auto mt-10 p-6">
        <AdminSignIn onLogin={login}></AdminSignIn>
      </div>
    );
  }
  else {
    return
  }
}

export default AdminDashboard;