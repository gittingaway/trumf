import React, { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
} from "@tanstack/react-table";
import styles from "./MerchantTable.module.css";

interface Merchant {
  id: number;
  name: string;
  cashback: string;
  image_url: string;
}

interface MerchantTableProps {
  merchants: Merchant[];
}

const MerchantTable: React.FC<MerchantTableProps> = ({ merchants }) => {
  const [sorting, setSorting] = useState([]);

  const columns = useMemo(
    () => [
      {
        accessorKey: "name",
        header: "Forretning",
        cell: ({ row }: any) => (
          <div className={styles.merchantName}>
            <img
              src={row.original.image_url}
              alt={`${row.original.name} logo`}
              className="" // Style the image to be circular with some margin
              loading="lazy"
            />
            {row.original.name}
          </div>
        ),
      },
      {
        accessorKey: "cashback",
        header: ({ header }) => <div className={styles.cashback}>Cashback</div>,
        cell: ({ row }: any) => (
          <div className={styles.cashback}>{row.original.cashback}</div>
        ),
      },
    ],
    [],
  );

  // Initialize table instance
  const table = useReactTable({
    data: merchants,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <table className={styles.table}>
      <thead className={styles.header}>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id} className={styles.tr}>
            {headerGroup.headers.map((header) => (
              <th
                key={header.id}
                className={styles.cashback}
                onClick={header.column.getToggleSortingHandler()}
              >
                {header.column.getIsSorted()
                  ? header.column.getIsSorted() === "asc"
                    ? " 🔼"
                    : " 🔽"
                  : ""}
                {flexRender(
                  header.column.columnDef.header,
                  header.getContext(),
                )}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody className={styles.tableBody}>
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id} className={styles.tableRow}>
            {row.getVisibleCells().map((cell) => (
              <td key={cell.id} className={styles.td}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default MerchantTable;
