import { TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { flexRender } from "@tanstack/react-table";
import type { HeaderGroup } from "@tanstack/react-table";


export interface HeaderTableProps {
  tableHeaderGroups: HeaderGroup<any>[];
}

export function HeaderTable({ tableHeaderGroups }: HeaderTableProps) {
  return (
    <TableHeader className="bg-muted sticky top-0 z-10">
      {tableHeaderGroups.map((headerGroup) => (
        <TableRow key={headerGroup.id}>
          {headerGroup.headers.map((header) => {
            return (
              <TableHead key={header.id} colSpan={header.colSpan}>
                {header.isPlaceholder
                  ? null
                  : flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
              </TableHead>
            );
          })}
        </TableRow>
      ))}
    </TableHeader>
  );
}
