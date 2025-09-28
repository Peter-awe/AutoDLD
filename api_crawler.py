#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime, timedelta
import logging
from config import Config

class APICrawler:
    """通过学术API获取真实文章数据"""
    
    def __init__(self):
        self.config = Config()
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.config.PATHS['logs_dir']}/api_crawler.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_real_articles(self):
        """通过API获取真实文章数据"""
        all_articles = []
        
        # 尝试不同的API源
        api_sources = [
            self.get_arxiv_articles,
            self.get_pubmed_articles,
            self.get_crossref_articles
        ]
        
        for api_func in api_sources:
            try:
                articles = api_func()
                if articles:
                    all_articles.extend(articles)
                    self.logger.info(f"从 {api_func.__name__} 获取到 {len(articles)} 篇文章")
                    break  # 如果从一个API获取成功，就停止尝试其他API
            except Exception as e:
                self.logger.warning(f"API调用失败 {api_func.__name__}: {str(e)}")
                continue
        
        return all_articles
    
    def get_arxiv_articles(self):
        """从arXiv获取AI/机器学习相关文章"""
        articles = []
        
        # arXiv API查询参数 - 专注于儿童言语障碍DLD相关
        query_terms = [
            "developmental language disorder",
            "child language impairment",
            "speech language pathology children",
            "language development disorder",
            "specific language impairment",
            "childhood apraxia of speech",
            "pediatric communication disorders",
            "language delay children",
            "speech therapy children",
            "bilingual language disorders",
            "language disorder children"
        ]
        
        for term in query_terms:
            try:
                url = "http://export.arxiv.org/api/query"
                params = {
                    'search_query': f'all:"{term}"',
                    'start': 0,
                    'max_results': 5,
                    'sortBy': 'submittedDate',
                    'sortOrder': 'descending'
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                # 解析arXiv的Atom格式响应
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                # arXiv的命名空间
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                
                for entry in root.findall('atom:entry', ns):
                    try:
                        title = entry.find('atom:title', ns).text.strip()
                        summary = entry.find('atom:summary', ns).text.strip() if entry.find('atom:summary', ns) is not None else ""
                        link = entry.find('atom:id', ns).text
                        published = entry.find('atom:published', ns).text
                        
                        # 检查日期是否在范围内
                        article_date = datetime.fromisoformat(published.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                        if self.is_within_date_range(article_date):
                            articles.append({
                                'title': title,
                                'abstract': summary[:300] if summary else "摘要暂不可用",
                                'link': link,
                                'date': article_date,
                                'journal': 'arXiv',
                                'source': 'arxiv'
                            })
                    except Exception as e:
                        self.logger.warning(f"解析arXiv文章失败: {str(e)}")
                        continue
                
                time.sleep(1)  # 避免请求过快
                
            except Exception as e:
                self.logger.error(f"arXiv API调用失败: {str(e)}")
                continue
        
        return articles[:10]  # 限制数量
    
    def get_pubmed_articles(self):
        """从PubMed获取医学相关文章"""
        articles = []
        
        # PubMed搜索关键词 - 专注于儿童言语障碍DLD相关
        search_terms = [
            "developmental language disorder children",
            "specific language impairment",
            "child language impairment",
            "pediatric speech disorders",
            "language delay children",
            "childhood apraxia of speech",
            "bilingual language disorders children",
            "speech therapy pediatric",
            "communication disorders children",
            "language disorder children"
        ]
        
        for term in search_terms:
            try:
                # PubMed E-utilities API
                base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
                
                # 搜索文章
                search_url = f"{base_url}esearch.fcgi"
                search_params = {
                    'db': 'pubmed',
                    'term': term,
                    'retmode': 'json',
                    'retmax': 5,
                    'sort': 'relevance',
                    'field': 'title'
                }
                
                search_response = requests.get(search_url, params=search_params, timeout=30)
                search_response.raise_for_status()
                search_data = search_response.json()
                
                article_ids = search_data.get('esearchresult', {}).get('idlist', [])
                
                if article_ids:
                    # 获取文章详情
                    fetch_url = f"{base_url}efetch.fcgi"
                    fetch_params = {
                        'db': 'pubmed',
                        'id': ','.join(article_ids),
                        'retmode': 'xml'
                    }
                    
                    fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
                    fetch_response.raise_for_status()
                    
                    # 解析PubMed XML
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(fetch_response.content)
                    
                    for article in root.findall('.//PubmedArticle'):
                        try:
                            # 提取标题
                            title_elem = article.find('.//ArticleTitle')
                            title = title_elem.text if title_elem is not None else "无标题"
                            
                            # 提取摘要
                            abstract_elem = article.find('.//AbstractText')
                            abstract = abstract_elem.text if abstract_elem is not None else "摘要暂不可用"
                            
                            # 提取日期
                            pub_date_elem = article.find('.//PubDate/Year')
                            pub_year = pub_date_elem.text if pub_date_elem is not None else datetime.now().year
                            
                            # 生成链接
                            article_id_elem = article.find('.//ArticleId[@IdType="pubmed"]')
                            article_id = article_id_elem.text if article_id_elem is not None else ""
                            link = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}" if article_id else ""
                            
                            articles.append({
                                'title': title,
                                'abstract': abstract[:300] if abstract else "摘要暂不可用",
                                'link': link,
                                'date': f"{pub_year}-01-01",  # PubMed日期精度较低
                                'journal': 'PubMed',
                                'source': 'pubmed'
                            })
                            
                        except Exception as e:
                            self.logger.warning(f"解析PubMed文章失败: {str(e)}")
                            continue
                
                time.sleep(1)  # 避免请求过快
                
            except Exception as e:
                self.logger.error(f"PubMed API调用失败: {str(e)}")
                continue
        
        return articles[:10]
    
    def get_crossref_articles(self):
        """从Crossref获取跨学科学术文章"""
        articles = []
        
        search_terms = [
            "developmental language disorder",
            "child language impairment",
            "speech therapy children",
            "pediatric communication disorders",
            "language delay children",
            "specific language impairment",
            "bilingual language disorders",
            "childhood apraxia of speech",
            "speech language pathology",
            "language disorder children"
        ]
        
        for term in search_terms:
            try:
                url = "https://api.crossref.org/works"
                params = {
                    'query': term,
                    'rows': 5,
                    'sort': 'relevance',
                    'filter': 'from-pub-date:2023'
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                for item in data.get('message', {}).get('items', []):
                    try:
                        title = item.get('title', ['无标题'])[0]
                        abstract = item.get('abstract', '摘要暂不可用')
                        link = item.get('URL', '')
                        published = item.get('published', {}).get('date-parts', [[2023, 1, 1]])[0]
                        
                        # 格式化日期
                        if len(published) >= 3:
                            date_str = f"{published[0]}-{published[1]:02d}-{published[2]:02d}"
                        else:
                            date_str = f"{published[0]}-01-01"
                        
                        journal = item.get('container-title', ['未知期刊'])[0]
                        
                        articles.append({
                            'title': title,
                            'abstract': abstract[:300] if abstract else "摘要暂不可用",
                            'link': link,
                            'date': date_str,
                            'journal': journal,
                            'source': 'crossref'
                        })
                        
                    except Exception as e:
                        self.logger.warning(f"解析Crossref文章失败: {str(e)}")
                        continue
                
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Crossref API调用失败: {str(e)}")
                continue
        
        return articles[:10]
    
    def is_within_date_range(self, date_str):
        """检查日期是否在指定范围内"""
        try:
            article_date = datetime.strptime(date_str, '%Y-%m-%d')
            start_date, end_date = self.config.get_date_range()
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            
            return start_date_obj <= article_date <= end_date_obj
        except Exception:
            return True  # 如果日期解析失败，默认包含
    
    def crawl_journals(self):
        """主爬取函数 - 不使用模拟数据"""
        self.logger.info("开始通过API获取真实文章数据")
        
        articles = self.get_real_articles()
        
        if not articles:
            self.logger.warning("未从任何API获取到文章数据")
            return []  # 返回空列表，而不是模拟数据
        
        self.logger.info(f"从API获取到 {len(articles)} 篇真实文章")
        return articles

if __name__ == "__main__":
    # 测试API爬虫
    crawler = APICrawler()
    articles = crawler.crawl_journals()
    print(f"获取到 {len(articles)} 篇真实文章")
    for article in articles[:3]:
        print(f"标题: {article['title']}")
        print(f"期刊: {article['journal']}")
        print(f"链接: {article['link']}")
        print(f"摘要: {article['abstract'][:100]}...")
        print("---")
