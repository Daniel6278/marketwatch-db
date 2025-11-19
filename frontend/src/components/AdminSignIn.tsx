import React from "react";
import { useForm } from "react-hook-form";
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "../components/ui/form";
import { Link } from "react-router-dom";

interface LoginProps {
  onLogin?: (username: string, password: string) => void;
}

interface LoginFormValues {
  username: string;
  password: string;
}

const AdminSignIn: React.FC<LoginProps> = ({ onLogin }) => {
  const form = useForm<LoginFormValues>({
    defaultValues: {
      username: "",
      password: "",
    },
    mode: "onBlur",
  });

  const handleSubmit = (values: LoginFormValues) => {
    console.log("Form submitted:", values);
    if (onLogin) onLogin(values.username, values.password);
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-5">Admin Sign In</h2>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Username</FormLabel>
                <FormControl>
                  <Input type="text" placeholder="admin123" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input type="password" placeholder="••••••••" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button type="submit" className="w-full" variant="default">
            Go
          </Button>
        </form>
      </Form>
    </div>
  );
};

export default AdminSignIn;
