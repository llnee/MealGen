DROP SCHEMA IF EXISTS nix CASCADE;
CREATE SCHEMA nix;

DROP TABLE IF EXISTS nix.foods CASCADE;
CREATE TABLE nix.foods (
    tag_id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    serving_unit TEXT NOT NULL,
    serving_qty INT NOT NULL,
    photo TEXT NOT NULL,
    locale TEXT NOT NULL
);
INSERT INTO nix.foods VALUES (690, 'mozzarella', 'oz', 1, 'https://nix-tag-images.s3.amazonaws.com/690_thumb.jpg', 'en_US');

DROP TABLE IF EXISTS nix.users CASCADE;
CREATE TABLE nix.users (
  uid INTEGER PRIMARY KEY NOT NULL,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  tel TEXT NOT NULL
);