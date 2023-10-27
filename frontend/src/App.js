import './App.css';
import React, { useState } from "react";
import { useNavigate, createSearchParams } from "react-router-dom";
import { Input, Layout, AutoComplete } from 'antd';
import { Helmet } from 'react-helmet';
import axios from "axios";
import debounce from 'lodash/debounce';

const { Search } = Input;

function App() {
  const { Content } = Layout;
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  
  const fetchProductSuggestions = debounce(async (value) => {
    try {
      const response = await axios.get('/api/products', { params: { search: value } });
      const products = response.data.map(product => product.name);
      // Filter suggestions based on both the first letter and partial string matching
      const firstLetter = value.charAt(0).toLowerCase();
      const suggestionsStartingWithFirstLetter = products.filter(product => product.charAt(0).toLowerCase() === firstLetter);
      // Filter the suggestions that partially match the user's input
      const partialMatchSuggestions = suggestionsStartingWithFirstLetter.filter(product => product.toLowerCase().includes(value.toLowerCase()));
      setSuggestions(partialMatchSuggestions);
    } catch (err) {
      console.error(err);
    }
  }, 0); // Adjust the debounce delay as needed

  const onSearch = (value) => {
    if (value === '') {
      // If the input is empty, clear the input field and suggestions
      setSearchValue('');
      setSuggestions([]);
    } else {
      const params = { keyword: value };
      navigate({
        pathname: "/search",
        search: `?${createSearchParams(params)}`,
      });
    }
  };

  const handleInputChange = (value) => {
    setSearchValue(value);
    fetchProductSuggestions(value);
  };

  const onSelect = (value) => {
    setSearchValue(value);
    onSearch(value);
  };

  const TITLE = 'Web Bot for Consumer Product Reviews'

  return (
    <div className="App">
        <Helmet>
          <title>{ TITLE }</title>
        </Helmet>
        <Layout className="content">
          <Layout>
          <Content>
          <div id="searchBar">
            {/* source: https://icons8.com/icon/xaquNfre75yC/robot */}
            <img width="64" height="64" src="https://img.icons8.com/nolan/96/bot.png" alt="bot"/>
              <AutoComplete
                value={searchValue}
                dataSource={suggestions}
                style={{ width: '100%', textAlign:"left" ,lineHeight:"40px"}}
                onSearch={handleInputChange}
                onSelect={onSelect}
                placeholder="Search for a product"

              >
                <Search
                  allowClear
                  enterButton="Search"
                  size="large"
                  onSearch={onSearch}
                />
              </AutoComplete>
          </div>
          </Content>
          </Layout>
          {/* <Footer className='footer' style={{ textAlign: 'center' }}>
            Created by CS18-2
          </Footer> */}
        </Layout>
      
    </div>

  );
}

export default App;
