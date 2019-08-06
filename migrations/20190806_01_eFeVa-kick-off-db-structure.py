"""
Kick off db structure
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE companies (
          id serial NOT NULL,
          company_name CHARACTER VARYING(512) DEFAULT ''::character varying,          
          created timestamp without time zone DEFAULT NULL,

          CONSTRAINT companies_id PRIMARY KEY (id) 
        );        
    """),
    step("""
        CREATE TABLE companies_contact_pages (
          id serial NOT NULL,
          company_id  int NOT NULL,
          url CHARACTER VARYING(512) DEFAULT ''::character varying,
          created timestamp without time zone DEFAULT NULL,
          CONSTRAINT companies_contact_page_id PRIMARY KEY (id) 
        );        
    """),
    step("""
        CREATE INDEX companies_contact_pages_company_id_index ON companies_contact_pages USING btree (company_id);
    """)
]
