import "./SearchResults.css";
import React, { useState, useEffect, useRef } from "react";
import { useNavigate, createSearchParams } from "react-router-dom";
import { SearchOutlined } from "@ant-design/icons";
import {Table, Breadcrumb, Input, Space, Button, Pagination} from "antd";
import axios from "axios";
import Highlighter from "react-highlight-words";
import {Helmet} from "react-helmet";
import { useQuery } from "react-query";
import {current} from "@reduxjs/toolkit";

function SearchResults() {
  const [products, setProducts] = useState([]);
  const navigate = useNavigate();
  const url = window.location.search;
  const urlParams = new URLSearchParams(url);
  const keyword = urlParams.get("keyword");
  const [searchText, setSearchText] = useState("");
  const [searchedColumn, setSearchedColumn] = useState("");
  const searchInput = useRef(null);
  const [pageSize, setPageSize] = useState(10);
  const [pageNumber, setPageNumber] = useState(1);
  const [resultTotal, setResultTotal] = useState();




  // const handleSearch = (selectedKeys, confirm, dataIndex) => {
  //   confirm();
  //   setSearchText(selectedKeys[0]);
  //   setSearchedColumn(dataIndex);
  // };
  // const handleReset = (clearFilters) => {
  //   clearFilters();
  //   setSearchText("");
  // };
  const getData = (pageNumber, pageSize) =>{
      if (keyword){
          axios.get('/api/products/'+keyword+'/'+pageNumber+'/'+pageSize)
          .then((res)=>{
              setResultTotal(res.data.slice(-1)[0].total)
              setProducts(res.data.slice(0,-1))
          })
      .catch((err) => console.log(err));
      }
      else{
          axios.get('/api/products/*'+'/'+pageNumber+'/'+pageSize)
          .then((res)=>{
              setResultTotal(res.data.slice(-1)[0].total)
              setProducts(res.data.slice(0,-1))
          })
      .catch((err) => console.log(err));
      }
  }

  // fetch data from backend through axios
  useEffect(() => {
      getData(pageNumber,pageSize)
  }, [keyword]);

  // search function for columns
  // const getColumnSearchProps = (dataIndex) => ({
  //   filterDropdown: ({
  //     setSelectedKeys,
  //     selectedKeys,
  //     confirm,
  //     clearFilters,
  //     close,
  //   }) => (
  //     <div
  //       style={{
  //         padding: 8,
  //       }}
  //       onKeyDown={(e) => e.stopPropagation()}
  //     >
  //       <Input
  //         ref={searchInput}
  //         placeholder={`Search ${dataIndex}`}
  //         value={selectedKeys[0]}
  //         onChange={(e) =>
  //           setSelectedKeys(e.target.value ? [e.target.value] : [])
  //         }
  //         onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
  //         style={{
  //           marginBottom: 8,
  //           display: "block",
  //         }}
  //       />
  //       <Space>
  //         <Button
  //           type="primary"
  //           onClick={() => handleSearch(selectedKeys, confirm, dataIndex)}
  //           icon={<SearchOutlined />}
  //           size="small"
  //           style={{
  //             width: 90,
  //           }}
  //         >
  //           Search
  //         </Button>
  //         <Button
  //           onClick={() => clearFilters && handleReset(clearFilters)}
  //           size="small"
  //           style={{
  //             width: 90,
  //           }}
  //         >
  //           Reset
  //         </Button>
  //         <Button
  //           type="link"
  //           size="small"
  //           onClick={() => {
  //             confirm({
  //               closeDropdown: false,
  //             });
  //             setSearchText(selectedKeys[0]);
  //             setSearchedColumn(dataIndex);
  //           }}
  //         >
  //           Filter
  //         </Button>
  //         <Button
  //           type="link"
  //           size="small"
  //           onClick={() => {
  //             close();
  //           }}
  //         >
  //           close
  //         </Button>
  //       </Space>
  //     </div>
  //   ),
  //   filterIcon: (filtered) => (
  //     <SearchOutlined
  //       style={{
  //         color: filtered ? "#1677ff" : undefined,
  //       }}
  //     />
  //   ),
  //   onFilter: (value, record) =>
  //     record[dataIndex].toString().toLowerCase().includes(value.toLowerCase()),
  //   onFilterDropdownOpenChange: (visible) => {
  //     if (visible) {
  //       setTimeout(() => searchInput.current?.select(), 100);
  //     }
  //   },
  //   render: (text) =>
  //     searchedColumn === dataIndex ? (
  //       <Highlighter
  //         highlightStyle={{
  //           backgroundColor: "#ffc069",
  //           padding: 0,
  //         }}
  //         searchWords={[searchText]}
  //         autoEscape
  //         textToHighlight={text ? text.toString() : ""}
  //       />
  //     ) : (
  //       text
  //     ),
  // });

  // number of products in the list
  const funcTotal = (total) => `Total ${resultTotal} products`;
  // columns in the table
  const columns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      // sorter: (a, b) => a.name.localeCompare(b.name),
      // ...getColumnSearchProps("name"),
    },
    {
      title: "Brand",
      dataIndex: "brand",
      key: "brand",
      // sorter: (a, b) => a.brand.localeCompare(b.brand),
      // ...getColumnSearchProps("brand"),
    },
    {
      title: "Category",
      dataIndex: "category",
      key: "category",
      // sorter: (a, b) => a.category.localeCompare(b.category),
      // ...getColumnSearchProps("category"),
    },

  ];

  return (
    <div className="SearchResults">

        <Helmet>
          <title>{ 'Search Results' }</title>
        </Helmet>
      <Breadcrumb
        id="breadcrumb"
        items={[
          {
            href: "/",
            title: (
              <>
                <SearchOutlined />
                <span>Search</span>
              </>
            ),
          },
          {
            title: "Products",
          },
        ]}
      />
      <Table
          pagination={{
            onChange:(page,pageSize)=> {
                setPageNumber(page);
                setPageSize(pageSize);
                getData(page,pageSize)

            },
          showSizeChanger: true,
          pageSizeOptions: [10, 20, 50, 100],
          showQuickJumper: true,
          showTotal: funcTotal,
            total : resultTotal,
        }}
        columns={columns}
        dataSource={products}
        rowKey="name"
        onRow={(record, rowIndex) => {
          return {
            onClick: (event) => {
              // console.log(record);
              const params = { product: record.id };
              navigate({
                pathname: "/products",
                search: `?${createSearchParams(params)}`,
              });
            }, // click row
          };
        }}
      />


    </div>
  );
}

export default SearchResults;
