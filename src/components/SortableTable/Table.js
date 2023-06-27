import React from "react";
import { useTable, useSortBy } from "react-table";
import "./style.css";

const defaultPropGetter = () => ({});

const NestedTable = ({ data }) => {
  const renderTableCell = (value) => {
    if (typeof value === "object") {
      return <NestedTable data={value} />;
    }
    return value;
  };

  return (
    <table>
      <tbody>
        {Object.entries(data).map(([key, value]) => (
          <tr key={key}>
            <td>{key}</td>
            <td>{renderTableCell(value)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const TableComponent = ({
  columns,
  data,
  getHeaderProps = defaultPropGetter,
  getColumnProps = defaultPropGetter
}) => {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow
  } = useTable(
    {
      columns,
      data,
    },
    useSortBy
  );

  return (
    <div className="table-container">
      <div className="table-wrapper">
        <table {...getTableProps()}>
          <thead className="sticky-headers">
            {headerGroups.map(headerGroup => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map(column => (
                  <th
                    {...column.getHeaderProps([
                      {
                        className: column.className
                      },
                      getHeaderProps(column),
                      getColumnProps(column),
                      column.getSortByToggleProps()
                    ])}
                  >
                    {column.render("Header")}
                    <span>{column.isSorted ? (column.isSortedDesc ? ' ▼' : ' ▲') : ''}</span>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row, i) => {
              prepareRow(row);
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map(cell => {
                    return (
                      <td
                        {...cell.getCellProps([
                          {
                            className: cell.column.className,
                            style: cell.column.style
                          },
                          getColumnProps(cell.column)
                        ])}
                      >
                        {typeof cell.value === "object" ? (
                          <NestedTable data={cell.value} />
                        ) : (
                          cell.render("Cell")
                        )}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TableComponent;
