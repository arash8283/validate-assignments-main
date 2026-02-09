# Assignment Validation

- [x] Basic assignment check based on input & outputs.
- [ ] Also option for duplicate code based on comparing checksum (calculated using sha256).

## Usage

### Setting Up

Place the assignments files (all c files) in the `assets` directory.
The filenames are the signature for generated report!

Build image:

```sh
docker compose build
```

Run image:

```sh
docker compose up
```

Delete Image (After using it):

```sh
docker compose down
```

### Getting Started

Put Your Solution JSON file in assets folder like `assets/solution.json` with this format:

```json
{
  "input": ["my input param1", "my input param2"],
  "output": ["line1", "line2"]
}
```

Also put all the `.c` source files in assets folder.

Run the image, Check the generated `Reports.md` In your assets folder.

## License

This project is unlicensed.
