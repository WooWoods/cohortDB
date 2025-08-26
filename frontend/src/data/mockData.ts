export type User = {
  id: string;
  name: string;
  email: string;
  role: "Admin" | "User" | "Editor";
  status: "Active" | "Inactive" | "Pending";
};

export const mockData: User[] = [
  { id: "1", name: "John Doe", email: "john.doe@example.com", role: "Admin", status: "Active" },
  { id: "2", name: "Jane Smith", email: "jane.smith@example.com", role: "User", status: "Active" },
  { id: "3", name: "Peter Jones", email: "peter.jones@example.com", role: "Editor", status: "Inactive" },
  { id: "4", name: "Mary Johnson", email: "mary.johnson@example.com", role: "User", status: "Pending" },
  { id: "5", name: "David Brown", email: "david.brown@example.com", role: "User", status: "Active" },
  { id: "6", name: "Susan Williams", email: "susan.williams@example.com", role: "Editor", status: "Active" },
  { id: "7", name: "Michael Miller", email: "michael.miller@example.com", role: "Admin", status: "Inactive" },
  { id: "8", name: "Linda Davis", email: "linda.davis@example.com", role: "User", status: "Active" },
  { id: "9", name: "Robert Garcia", email: "robert.garcia@example.com", role: "User", status: "Pending" },
  { id: "10", name: "Patricia Rodriguez", email: "patricia.rodriguez@example.com", role: "Editor", status: "Active" },
];