import { useEffect, useState } from "react";
import { getUsers, approveUser, rejectUser, User } from "@/services/api";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useAuth } from "@/context/AuthContext";
import { toast } from "sonner";

export function Admin() {
  const { token } = useAuth();
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    if (token) {
      getUsers(token)
        .then(setUsers)
        .catch(() => {
          // Error is handled in api.ts
        });
    }
  }, [token]);

  const handleApprove = async (userId: number) => {
    if (token) {
      try {
        await approveUser(userId, token);
        setUsers(users.map((user) =>
          user.id === userId ? { ...user, status: "approved" } : user
        ));
        toast.success("User approved");
      } catch (error) {
        // Error is handled in api.ts
      }
    }
  };

  const handleReject = async (userId: number) => {
    if (token) {
      try {
        await rejectUser(userId, token);
        setUsers(users.map((user) =>
          user.id === userId ? { ...user, status: "rejected" } : user
        ));
        toast.success("User rejected");
      } catch (error) {
        // Error is handled in api.ts
      }
    }
  };

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Username</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map((user) => (
            <TableRow key={user.id}>
              <TableCell>{user.username}</TableCell>
              <TableCell>{user.email}</TableCell>
              <TableCell>{user.status}</TableCell>
              <TableCell>
                {user.status === "pending" && (
                  <>
                    <Button onClick={() => handleApprove(user.id)} className="mr-2">
                      Approve
                    </Button>
                    <Button onClick={() => handleReject(user.id)} variant="destructive">
                      Reject
                    </Button>
                  </>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
