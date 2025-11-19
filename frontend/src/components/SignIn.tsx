import React from "react";
import { useForm, Controller } from "react-hook-form";
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
  onLogin?: (email: string, password: string) => void;
}

interface LoginFormValues {
  email: string;
  password: string;
}

const SignIn: React.FC<LoginProps> = ({ onLogin }) => {
  const form = useForm<LoginFormValues>({
    defaultValues: {
      email: "",
      password: "",
    },
    mode: "onBlur",
  });

  const handleSubmit = (values: LoginFormValues) => {
    console.log("Form submitted:", values);
    if (onLogin) onLogin(values.email, values.password);
  };

  return (
    <div className="min-w-[400px]">
      <h2 className="mb-5 font-bold">Sign In</h2>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input
                    type="email"
                    placeholder="you@example.com"
                    {...field}
                  />
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

      <hr className="my-4" />

      <h3 className="mb-3">Don’t have an account?</h3>
      <div>
        <Button asChild className="!text-white w-full">
          <Link to="/register">Create Your Account</Link>
        </Button>
      </div>
    </div>
  );
};

export default SignIn;
