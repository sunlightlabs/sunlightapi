CREATE INDEX lobbyists_bucket_fingerprint_year ON lobbyists_lobbyistbucket (bucket, year);
CREATE INDEX filing_registrant_name on lobbyists_filing (registrant_name);
CREATE INDEX filing_client_name on lobbyists_filing (client_name);

