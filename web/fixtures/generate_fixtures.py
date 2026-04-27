def main():
    with open('meva_fixture.json', 'w', encoding='utf-8') as f:
        json.dump(dades, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()