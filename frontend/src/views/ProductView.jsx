import './ProductView.css';
import * as React from "react";
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchOutlined, ShoppingOutlined, StarOutlined, SmileOutlined, BarChartOutlined, LoadingOutlined, BulbOutlined } from '@ant-design/icons';
import { Space, Breadcrumb, Divider, Descriptions, List, Tag, Menu, Progress, Col, Row } from 'antd';
import { Bar } from '@ant-design/plots';
import axios from "axios";
import { Empty } from 'antd';
import {Helmet} from "react-helmet";
const { CheckableTag } = Tag;


function ProductView() {
    const TITLE = 'Web Bot for Consumer Product Reviews'
  const [product, setProduct] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [positivePlot, setPositivePlot] = useState([]);
  const [negativePlot, setNegativePlot] = useState([]);
  const [pairPlot, setPairPlot] = useState([]);
  const [ratingDic, setRatingDic] = useState([]);
  const [aspectDic, setAspectDic] = useState([]);

  const onShowSizeChange = (current, pageSize) => {
      console.log(current, pageSize);
  };
  const [keywords, setKeywords] = useState([]);
  const [summary, setSummary] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);

  const navigate = useNavigate();

  const url = window.location.search;
  const urlParams = new URLSearchParams(url);
  const productId = urlParams.get('product');


  const handleChange = (tag, checked) => {
    const nextSelectedTags = checked
      ? [tag]
      : []
    setSelectedTags(nextSelectedTags);

    if (nextSelectedTags.length != 0) {
      axios
      .get('/api/getReviewsByKeyword/' + productId + "/" + nextSelectedTags[0])
      .then((res) => {
        setReviews(res.data);
      })
      .catch((err) => console.log(err));
    } else {
      getAllReviews();

    }
    
  };


  const getAllReviews = () => axios
    .get('/api/getReviewsByProductId/' + productId)
    .then((res) => {
      setReviews(res.data);
    })
    .catch((err) => console.log(err));
  
  const getSummary = () => axios
    .get('/api/getSummaryByProductId/' + productId)
    .then((res) => {
      setSummary(res.data);
    })
    .catch((err) => console.log('getSummary',err));

    const getFeatureVisual = () => axios
          .get('/api/getFeatureVisualByProductId/'+productId)
          .then((res) => {
            setPositivePlot(res.data.positive)
            setNegativePlot(res.data.negative)
            setPairPlot(res.data.pairs)
          })
          .catch((err) => console.log('getFeature',err));

  const IconText = ({ icon, text }) => (
    <Space>
      {React.createElement(icon)}
      {text}
    </Space>
  );

  useEffect(() => {
        // Get rating data of the product
        axios.get('/api/getRatingBI/' + productId)
        .then((res) => {
            // console.log('rating',res.data)
            setRatingDic(res.data);
        })
        .catch((err) => console.log('ratingDic',err));

        axios.get('/api/getAspectBI/' + productId)
        .then((res) => {
          setAspectDic(res.data);
        })
        .catch((err) => console.log('AspectBI',err));


    axios
      .get('/api/getProductById/' + productId)
      .then((res) => {
        setProduct(res.data);
      })
      .catch((err) => console.log('product',err));

      axios
      .get('/api/getKeywordsByProductId/' + productId)
      .then((res) => {
        setKeywords(res.data);
      })
      .catch((err) => console.log('product by keyword',err));
    getFeatureVisual()

    getAllReviews();
    // getSummary();
  }, [productId]); 

  const items = [
    {
      key: '1',
      label: 'Brand',
      children: product.brand,
    },
    {
      key: '2',
      label: 'Category',
      children: product.category,
    },
    {
        key: '3',
        label: 'Description',
        span: 2,
        children: product.description,
    },
    
  ];
  const funcTotal = (total) => `Total ${total} reviews`

  const menuItems = [
    {
      label: 'Reviews',
      key: 'reviews',
      icon: <SmileOutlined />,
    },
    {
      label: 'Business Insights',
      key: 'bi',
      icon: <BulbOutlined />,
    },
    {
      label: 'Plots',
      key: 'plots',
      icon: <BarChartOutlined />,
    },
    ]

  const [current, setCurrent] = useState('reviews');
  const onMenuClick = (e) => {
    setCurrent(e.key);
  };

  function ShowComponent() {
    if (current == "reviews") {
      return <Reviews />;
    } else if (current == "bi") {
      return <BI />;
    } else if (current == "plots") {
      return <Plots />;
    }
  }

  const spinIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;

  function Plots() {
    const positiveData = positivePlot.slice(0, 10);
    const positiveConfig = {
      data: positiveData,
      xField: 'frequency',
      yField: 'pairs',
      seriesField: 'pairs',
      legend: {
        position: 'top-left',
      },
    };
    const negativeData = negativePlot.slice(0, 10);
    const negativeConfig = {
      data: negativeData,
      xField: 'frequency',
      yField: 'pairs',
      seriesField: 'pairs',
      legend: {
        position: 'top-left',
      },
    };
    const pairData = pairPlot.slice(0, 10);
    const pairConfig = {
      data: pairData,
      xField: 'frequency',
      yField: 'pairs',
      seriesField: 'pairs',
      legend: {
        position: 'top-left',
      },
    };
    
    return (
      <div>
                      <Helmet>
                <title>{'Business Insight Visualization'  }</title>
            </Helmet>
        <div className="chart">
          <span>Top 10 Positive Review Word Pairs</span>
            {positivePlot.length > 0 && <Bar {...positiveConfig} />}
            {positivePlot.length == 0 &&
                <Empty
                description={
                  <span>
                    No data or data size too small.
                  </span>
                }
              />}
        </div>
        {/*<div className="chart">*/}
        {/*  <span>Top 10 Negative Review Word Pairs</span>*/}
        {/*  {negativePlot.length > 0 && <Bar {...negativeConfig} />}*/}
        {/*  {negativePlot.length == 0 &&*/}
        {/*      <Empty*/}
        {/*       description={*/}
        {/*          <span>*/}
        {/*            No data or data size too small.*/}
        {/*          </span>*/}
        {/*        }*/}
        {/*      />}*/}

        {/*</div>*/}
        <div className="chart">
          <span>Top 10 Ngrams Review Word Pairs</span>
          {pairPlot.length > 0 &&<Bar {...pairConfig} />}
          {pairPlot.length == 0 &&
              <Empty
               description={
                  <span>
                    No data or data size too small.
                  </span>
                }
              />}
        </div>
      </div>
    );
  };

  function BI() {
    return (
      

      <div className="BI">
                      <Helmet>
                <title>{ 'Business Insight' }</title>
            </Helmet>
        {/* <Divider orientation="left" orientationMargin="0">
          Review Summarization
        </Divider>
        {summary.length == 0 ? <Spin indicator={spinIcon} /> : summary} */}

        {/* <img src={ratingImage} width={35+'%'}     style={{ margin: 'auto', display: 'flex'}}/>
        <img src={featureImage} width={100+'%'}     style={{ margin: 'auto', display: 'flex'}}/> */}
          <Divider orientation="left" orientationMargin="0">
        
        <Row>
          Positive rating ratio
        </Row>
        <br></br>
        <Row>
        <Space wrap>
          <Col>
            <Progress  type="circle" percent={ratingDic.ratingRatio} format={(percent) => `${ratingDic.ratingRatio}%` } />
          </Col>
          
          <Col>Number of Reviews: {ratingDic.numOfReviews}</Col>
        </Space>
        </Row>
        <br></br>
        <table className='table'>
            <tbody>
          <tr>
            <th>1 Star</th>
            <th>2 Stars</th>
            <th>3 Stars</th>
            <th>4 Stars</th>
            <th>5 Stars</th>
          </tr>
          <tr>
            <td><Progress type="circle" percent={ratingDic.oneStarRatio} format={(percent) => `${ratingDic.oneStarRatio}%`}/></td>
            <td><Progress type="circle" percent={ratingDic.twoStarRatio} format={(percent) => `${ratingDic.twoStarRatio}%`}/></td>
            <td><Progress type="circle" percent={ratingDic.threeStarRatio} format={(percent) => `${ratingDic.threeStarRatio}%`}/></td>
            <td><Progress type="circle" percent={ratingDic.fourStarRatio} format={(percent) => `${ratingDic.fourStarRatio}%`}/></td>
            <td><Progress type="circle" percent={ratingDic.fiveStarRatio} format={(percent) => `${ratingDic.fiveStarRatio}%`}/></td>
          </tr>
            </tbody>
        </table>
        <br></br>
        <Divider orientation="left" orientationMargin="0">Positive Features</Divider>
          <Divider orientation="left" orientationMargin="0">
            {aspectDic.positive != undefined && aspectDic.positive.map(word => (
              <Tag color="green">{word}</Tag>
            ))}
          </Divider>
          
          <Divider orientation="left" orientationMargin="0">Negative Features</Divider>
          <Divider orientation="left" orientationMargin="0">
            {aspectDic.negative != undefined && aspectDic.negative.map(word => (
                <Tag color="red">{word}</Tag>
              ))}
          </Divider>
          
        </Divider>
      </div>
    );
  }

  function Reviews() {
    return (

        <div className='reviewsComponent'>
            <Helmet>
                <title>{ 'Reviews' }</title>
            </Helmet>
        <div className="reviewHeader">
          <span
            style={{
              marginRight: 8,
            }}
          >
            Keyword:
          </span>
          <Space size={[0, 8]} wrap>
            {keywords.map((tag) => (
              <CheckableTag
                key={tag}
                checked={selectedTags.includes(tag)}
                onChange={(checked) => handleChange(tag, checked)}
              >
                {tag}
              </CheckableTag>
            ))}
          </Space>
        </div>
        <List
          itemLayout="horizontal"
          size="large"
          pagination={{
              showSizeChanger:true,
              pageSizeOptions: [10,20,50,100],
              showQuickJumper:true,
              showTotal: funcTotal

          }}
          dataSource={reviews}
          renderItem={(item) => (
            <List.Item
              key={item.id}
              actions={[
                <IconText icon={StarOutlined} text={item.rating} key="list-vertical-star-o" />,
              ]}
              // extra={
              //   <img
              //     width={272}
              //     alt="logo"
              //     src="https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png"
              //   />
              // }
            >
              <List.Item.Meta
                title={item.title}
                description={item.user + ' | ' + item.date + ' | ' + item.platform}
              />
              {item.text}
            </List.Item>
          )}
        />
    {/*<Pagination size="small" total={50} showSizeChanger showQuickJumper />*/}
    {/*<Pagination size="small" total={50} showTotal={showTotal} />*/}
        </div>
    );
}

  return (
    <div className='ProductView'>
        <Breadcrumb id='breadcrumb'
        items={[
          {
            href: '/',
            title: (
              <>
                <SearchOutlined />
                <span>Search</span>
              </>
            ),
          },
          {
            onClick: () => navigate(-1) ,
            href: null,
            title: (
              <>
                <ShoppingOutlined />
                <span>Products</span>
              </>
            ),

          },
          {
            title: product.name,
          },
        ]}
        />
        <Descriptions title={product.name} column={2} layout="vertical" items={items} />
        <Menu className="menu" onClick={onMenuClick} selectedKeys={[current]} mode="horizontal" items={menuItems} />
        <ShowComponent />
    </div>
    
  );
}

export default ProductView;
